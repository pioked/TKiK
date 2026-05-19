from antlr4.error.ErrorListener import ErrorListener

class MiniCalcError(Exception):
    pass

class SyntaxError(MiniCalcError):
    def __init__(self, message, line, column):
        super().__init__(f"Syntax Error [{line}:{column}]: {message}")

class SemanticError(MiniCalcError):
    pass

class RuntimeError(MiniCalcError):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(msg, line, column)
    
class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass