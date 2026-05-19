import sys
import os
from antlr4 import FileStream, CommonTokenStream

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.parser.generated.MiniCalcLangLexer import MiniCalcLangLexer
from src.parser.generated.MiniCalcLangParser import MiniCalcLangParser
from src.parser.build_ast import ASTBuilder
from src.interpreter.evaluator import InterpreterVisitor
from src.errors.exceptions import CustomErrorListener, MiniCalcError

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file.mcl>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    try:
        input_stream = FileStream(input_file, encoding='utf-8')
        lexer = MiniCalcLangLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(CustomErrorListener())
        
        token_stream = CommonTokenStream(lexer)

        parser = MiniCalcLangParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(CustomErrorListener())
        
        tree = parser.program()

        ast_builder = ASTBuilder()
        ast = ast_builder.visit(tree)

        interpreter = InterpreterVisitor()
        interpreter.visit(ast)

    except MiniCalcError as e:
        print(f"\nExecution failed with error:\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nCritical Runtime Error:\n{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()