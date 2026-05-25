from src.parser.generated.MiniCalcLangParser import MiniCalcLangParser
from src.parser.generated.MiniCalcLangVisitor import MiniCalcLangVisitor
from src.ast.nodes import *
import math

class ASTBuilder(MiniCalcLangVisitor):
    
    def visitProgram(self, ctx: MiniCalcLangParser.ProgramContext):
        statements = []
        for stmt in ctx.statement():
            statements.append(self.visit(stmt))
        return Program(statements)

    def visitConst_declaration(self, ctx: MiniCalcLangParser.Const_declarationContext):
        name = ctx.ID().getText()
        expr = self.visit(ctx.literal())
        return VarDeclNode(name, expr, is_const=True)

    def visitVar_declaration(self, ctx: MiniCalcLangParser.Var_declarationContext):
        name = ctx.ID().getText()
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDeclNode(name, expr, is_const=False)

    def visitBlock(self, ctx: MiniCalcLangParser.BlockContext):
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return BlockNode(statements)

    def visitDef_stmt(self, ctx: MiniCalcLangParser.Def_stmtContext):
        func_name = ctx.ID().getText()
        params = [id_node.getText() for id_node in ctx.parameter_list().ID()] if ctx.parameter_list() else []
        body = self.visit(ctx.block())
        return DefNode(func_name, params, body)

    def visitAssignment(self, ctx: MiniCalcLangParser.AssignmentContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        return AssignNode(var_name, value)

    def visitCompound_assignment(self, ctx: MiniCalcLangParser.Compound_assignmentContext):
        name = ctx.ID().getText()
        op = ctx.getChild(1).getText() 
        expr = self.visit(ctx.expr())
        return CompoundAssignNode(name, op, expr)

    def visitPrint_stmt(self, ctx: MiniCalcLangParser.Print_stmtContext):
        if ctx.expression_list():
            exprs = [self.visit(e) for e in ctx.expression_list().expr()]
            if len(exprs) == 1:
                return PrintNode(exprs[0])
            return PrintNode(ListNode(exprs))
        return PrintNode(NullNode())

    def visitIf_stmt(self, ctx: MiniCalcLangParser.If_stmtContext):
        conditions = [self.visit(e) for e in ctx.expr()]
        blocks = [self.visit(b) for b in ctx.block()]
        
        false_body = None
        if len(blocks) > len(conditions):
            false_body = blocks[-1]
            
        for i in range(len(conditions) - 1, 0, -1):
            elif_cond = conditions[i]
            elif_body = blocks[i]
            false_body = BlockNode([IfNode(elif_cond, elif_body, false_body)])
            
        return IfNode(conditions[0], blocks[0], false_body)

    def visitWhile_stmt(self, ctx: MiniCalcLangParser.While_stmtContext):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.block())
        return WhileNode(condition, body)

    def visitFor_stmt(self, ctx: MiniCalcLangParser.For_stmtContext):
        iterator_name = ctx.ID().getText()
        start_expr = self.visit(ctx.expr(0))
        end_expr = self.visit(ctx.expr(1))
        step_expr = self.visit(ctx.expr(2)) if len(ctx.expr()) > 2 else None
        body = self.visit(ctx.block())
        return ForNode(iterator_name, start_expr, end_expr, step_expr, body)

    def visitRepeat_until_stmt(self, ctx: MiniCalcLangParser.Repeat_until_stmtContext):
        block = self.visit(ctx.block())
        condition = self.visit(ctx.expr())
        return RepeatUntilNode(block, condition)

    def visitSwitch_stmt(self, ctx: MiniCalcLangParser.Switch_stmtContext):
        expr = self.visit(ctx.expr())
        cases = [self.visit(case_ctx) for case_ctx in ctx.case_branch()]
        default_block = self.visit(ctx.default_branch()) if ctx.default_branch() else None
        return SwitchNode(expr, cases, default_block)

    def visitCase_branch(self, ctx: MiniCalcLangParser.Case_branchContext):
        value = self.visit(ctx.literal())
        statement = self.visit(ctx.statement())
        return CaseNode(value, statement)

    def visitDefault_branch(self, ctx: MiniCalcLangParser.Default_branchContext):
        return self.visit(ctx.statement())

    def visitReturn_stmt(self, ctx: MiniCalcLangParser.Return_stmtContext):
        val = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnNode(val)

    def visitBreak_stmt(self, ctx: MiniCalcLangParser.Break_stmtContext):
        return BreakNode()

    def visitContinue_stmt(self, ctx: MiniCalcLangParser.Continue_stmtContext):
        return ContinueNode()

    def visitExpr_stmt(self, ctx: MiniCalcLangParser.Expr_stmtContext):
        return self.visit(ctx.expr())

    def visitMatrixExpr(self, ctx: MiniCalcLangParser.MatrixExprContext):
        matrix_ctx = ctx.matrix_expr()
        rows = []
        for row_ctx in matrix_ctx.matrix_row():
            row = [self.visit(expr) for expr in row_ctx.expr()]
            rows.append(row)
        return MatrixNode(rows)

    def visitListExpr(self, ctx: MiniCalcLangParser.ListExprContext):
        elements = [self.visit(e) for e in ctx.list_expr().expr()]
        return ListNode(elements)

    def visitParensExpr(self, ctx: MiniCalcLangParser.ParensExprContext):
        return self.visit(ctx.expr())

    def visitFuncCallExpr(self, ctx: MiniCalcLangParser.FuncCallExprContext):
        func_name = ctx.ID().getText()
        args = [self.visit(expr) for expr in ctx.expression_list().expr()] if ctx.expression_list() else []
        return FuncCallNode(func_name, args)

    def visitIndexExpr(self, ctx: MiniCalcLangParser.IndexExprContext):
        target = self.visit(ctx.expr())
        indices = [self.visit(e) for e in ctx.expression_list().expr()]
        return IndexNode(target, indices)

    def visitVarExpr(self, ctx: MiniCalcLangParser.VarExprContext):
        return VariableNode(ctx.ID().getText())

    def visitLiteralExpr(self, ctx: MiniCalcLangParser.LiteralExprContext):
        return self.visit(ctx.literal())

    def visitTransposeExpr(self, ctx: MiniCalcLangParser.TransposeExprContext):
        return UnaryOpNode("'", self.visit(ctx.expr()))

    def visitUnaryExpr(self, ctx: MiniCalcLangParser.UnaryExprContext):
        op = ctx.getChild(0).getText()
        return UnaryOpNode(op, self.visit(ctx.expr()))

    def visitPowerExpr(self, ctx: MiniCalcLangParser.PowerExprContext):
        return BinOpNode(self.visit(ctx.expr(0)), '^', self.visit(ctx.expr(1)))

    def visitMulDivExpr(self, ctx: MiniCalcLangParser.MulDivExprContext):
        op = ctx.getChild(1).getText()
        return BinOpNode(self.visit(ctx.expr(0)), op, self.visit(ctx.expr(1)))

    def visitAddSubExpr(self, ctx: MiniCalcLangParser.AddSubExprContext):
        op = ctx.getChild(1).getText()
        return BinOpNode(self.visit(ctx.expr(0)), op, self.visit(ctx.expr(1)))

    def visitRelationalExpr(self, ctx: MiniCalcLangParser.RelationalExprContext):
        op = ctx.getChild(1).getText()
        return BinOpNode(self.visit(ctx.expr(0)), op, self.visit(ctx.expr(1)))

    def visitAndExpr(self, ctx: MiniCalcLangParser.AndExprContext):
        return BinOpNode(self.visit(ctx.expr(0)), 'and', self.visit(ctx.expr(1)))

    def visitOrExpr(self, ctx: MiniCalcLangParser.OrExprContext):
        return BinOpNode(self.visit(ctx.expr(0)), 'or', self.visit(ctx.expr(1)))

    def visitLiteral(self, ctx: MiniCalcLangParser.LiteralContext):
        if ctx.NUMBER():
            text = ctx.NUMBER().getText()
            return NumberNode(float(text) if '.' in text else int(text))
        elif ctx.STRING():
            return StringNode(ctx.STRING().getText()[1:-1])
        elif ctx.KEYWORD_TRUE():
            return BoolNode(True)
        elif ctx.KEYWORD_FALSE():
            return BoolNode(False)
        elif ctx.KEYWORD_NULL():
            return NullNode()
        elif ctx.CONST_PI():
            return NumberNode(math.pi)
        elif ctx.CONST_E():
            return NumberNode(math.e)