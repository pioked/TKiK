from src.errors.exceptions import SemanticError

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def define_var(self, name: str, value):
        self.variables[name] = value

    def define_func(self, name: str, func_node):
        self.functions[name] = func_node

    def assign_var(self, name: str, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent is not None:
            self.parent.assign_var(name, value)
        else:
            raise SemanticError(f"Cannot assign to undefined variable: '{name}'")

    def get_var(self, name: str):
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get_var(name)
        raise SemanticError(f"Undefined variable: '{name}'")

    def get_func(self, name: str):
        if name in self.functions:
            return self.functions[name]
        if self.parent is not None:
            return self.parent.get_func(name)
        return None