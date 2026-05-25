import math
import numpy as np
from src.interpreter.environment import Environment
from src.errors.exceptions import SemanticError, RuntimeError, ReturnException, BreakException, ContinueException

class InterpreterVisitor:
    def __init__(self, env=None):
        self.env = env or Environment()

        self.env.define_var('pi', np.pi)
        self.env.define_var('e', np.e)

        self.builtins = {
            'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
            'sqrt': np.sqrt, 'log': np.log, 'exp': np.exp,
            'det': np.linalg.det, 'inv': np.linalg.inv
        }

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise RuntimeError(f'No visit method implementation for {type(node).__name__}')

    def visit_Program(self, node):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result

    def visit_BlockNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_BoolNode(self, node):
        return node.value

    def visit_VariableNode(self, node):
        return self.env.get_var(node.name)

    def visit_MatrixNode(self, node):
        evaluated_rows = [
            [self.visit(expr) for expr in row] 
            for row in node.rows
        ]
        return np.array(evaluated_rows, dtype=float)

    def visit_UnaryOpNode(self, node):
        val = self.visit(node.expr)
        if node.op == '-':
            return -val
        elif node.op == '+':
            return val
        elif node.op == 'not':
            return not val
        elif node.op == "'":
            if not isinstance(val, np.ndarray):
                raise SemanticError("Transpose operator (') can only be applied to matrices.")
            return np.transpose(val)

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        
        if node.op == 'and': return bool(left and self.visit(node.right))
        if node.op == 'or': return bool(left or self.visit(node.right))
        
        right = self.visit(node.right)

        try:
            if node.op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            if node.op == '-': return left - right
            if node.op == '*':
                if isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
                    return np.dot(left, right)
                return left * right
            if node.op == '/': 
                if right == 0: raise RuntimeError("Division by zero")
                return left / right
            if node.op == '%': return left % right
            if node.op == '^': return left ** right
            if node.op == '>': return left > right
            if node.op == '<': return left < right
            if node.op == '>=': return left >= right
            if node.op == '<=': return left <= right
            if node.op == '==': 
                if isinstance(left, np.ndarray) or isinstance(right, np.ndarray):
                    return np.array_equal(left, right)
                return left == right
            if node.op == '!=': 
                if isinstance(left, np.ndarray) or isinstance(right, np.ndarray):
                    return not np.array_equal(left, right)
                return left == right
        except Exception as e:
            raise RuntimeError(f"Operation failed: {str(e)}")

    def visit_AssignNode(self, node):
        val = self.visit(node.value)
        self.env.assign_var(node.var_name, val)
        return val

    def visit_PrintNode(self, node):
        val = self.visit(node.expression)
        if isinstance(val, bool):
            print("true" if val else "false")
        else:
            print(val)

    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.true_body)
        elif node.false_body is not None:
            self.visit(node.false_body)

    def visit_WhileNode(self, node):
        while self.visit(node.condition):
            try:
                self.visit(node.body)
            except BreakException:
                break
            except ContinueException:
                continue

    def visit_ForNode(self, node):
        start_val = self.visit(node.start_expr)
        end_val = self.visit(node.end_expr)
        step_val = self.visit(node.step_expr) if node.step_expr else 1
        
        self.env.define_var(node.iterator_name, start_val)
        
        while True:
            current_val = self.env.get_var(node.iterator_name)
            if step_val > 0 and current_val > end_val: break
            if step_val < 0 and current_val < end_val: break
            
            try:
                self.visit(node.body)
            except BreakException:
                break
            except ContinueException:
                pass
                
            self.env.define_var(node.iterator_name, self.env.get_var(node.iterator_name) + step_val)

    def visit_DefNode(self, node):
        self.env.define_func(node.func_name, node)

    def visit_ReturnNode(self, node):
        val = self.visit(node.value) if node.value else None
        raise ReturnException(val)

    def visit_FuncCallNode(self, node):
        if node.func_name in self.builtins:
            args = [self.visit(arg) for arg in node.args]
            try:
                return self.builtins[node.func_name](*args)
            except Exception as e:
                raise RuntimeError(f"Error calling built-in function '{node.func_name}': {e}")

        func_def = self.env.get_func(node.func_name)
        if not func_def:
            raise SemanticError(f"Function '{node.func_name}' is not defined")

        if len(node.args) != len(func_def.params):
            raise SemanticError(f"Function '{node.func_name}' expects {len(func_def.params)} arguments, got {len(node.args)}")

        func_env = Environment(parent=self.env)
        
        for param_name, arg_expr in zip(func_def.params, node.args):
            func_env.define_var(param_name, self.visit(arg_expr))

        previous_env = self.env
        self.env = func_env
        
        try:
            self.visit(func_def.body)
        except ReturnException as ret:
            self.env = previous_env
            return ret.value
        
        self.env = previous_env
        return None
    
    def visit_BreakNode(self, node):
        raise BreakException()

    def visit_ContinueNode(self, node):
        raise ContinueException()
    
    def visit_VarDeclNode(self, node):
        val = self.visit(node.expr) if node.expr else None
        self.env.define_var(node.name, val)
        return val

    def visit_CompoundAssignNode(self, node):
        current_val = self.env.get_var(node.name)
        val_to_apply = self.visit(node.expr)
        
        if node.operator == '+=': new_val = current_val + val_to_apply
        elif node.operator == '-=': new_val = current_val - val_to_apply
        elif node.operator == '*=': new_val = current_val * val_to_apply
        elif node.operator == '/=': new_val = current_val / val_to_apply
        else: new_val = current_val
        
        self.env.assign_var(node.name, new_val)
        return new_val

    def visit_RepeatUntilNode(self, node):
        while True:
            try:
                self.visit(node.block)
            except BreakException:
                break
            except ContinueException:
                pass
            
            condition = self.visit(node.condition)
            if condition:
                break

    def visit_SwitchNode(self, node):
        switch_val = self.visit(node.expr)
        matched = False
        
        for case in node.cases:
            case_val = self.visit(case.value)
            if switch_val == case_val:
                self.visit(case.statement)
                matched = True
                break
                
        if not matched and node.default_block:
            self.visit(node.default_block)

    def visit_ListNode(self, node):
        return [self.visit(element) for element in node.elements]

    def visit_IndexNode(self, node):
        target = self.visit(node.target)
        resolved_indices = tuple(int(self.visit(idx)) for idx in node.indices)
        try:
            if isinstance(target, np.ndarray):
                return target[resolved_indices]
            else:
                res = target
                for i in resolved_indices:
                    res = res[i]
                return res
        except (IndexError, TypeError, KeyError):
            raise RuntimeError(f"Index out of bounds or invalid indexing targets with paths: {resolved_indices}")

    def visit_NullNode(self, node):
        return None