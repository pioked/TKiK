from src.parser.generated.MiniCalcLangParser import MiniCalcLangParser
from src.parser.generated.MiniCalcLangVisitor import MiniCalcLangVisitor
from src.ast.nodes import *

class ASTBuilder(MiniCalcLangVisitor):
    
    def visitProgram(self, ctx: MiniCalcLangParser.ProgramContext):
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return Program(statements)

    def visitBlock(self, ctx: MiniCalcLangParser.BlockContext):
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return BlockNode(statements)

    def visitDef_stmt(self, ctx: MiniCalcLangParser.Def_stmtContext):
        func_name = ctx.ID(0).getText()
        params = [id_node.getText() for id_node in ctx.ID()[1:]]
        body = self.visit(ctx.block())
        return DefNode(func_name, params, body)

    def visitReturn_stmt(self, ctx: MiniCalcLangParser.Return_stmtContext):
        val = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnNode(val)

    def visitAssignment(self, ctx: MiniCalcLangParser.AssignmentContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        return AssignNode(var_name, value)

    def visitPrint_stmt(self, ctx: MiniCalcLangParser.Print_stmtContext):
        return PrintNode(self.visit(ctx.expr()))

    def visitIf_stmt(self, ctx: MiniCalcLangParser.If_stmtContext):
        condition = self.visit(ctx.expr())
        true_body = self.visit(ctx.block(0))
        false_body = self.visit(ctx.block(1)) if len(ctx.block()) > 1 else None
        return IfNode(condition, true_body, false_body)

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

    def visitExpr_stmt(self, ctx: MiniCalcLangParser.Expr_stmtContext):
        return self.visit(ctx.expr())

    def visitMatrixExpr(self, ctx: MiniCalcLangParser.MatrixExprContext):
        rows = []
        for row_ctx in ctx.matrix_row():
            row = [self.visit(expr) for expr in row_ctx.expr()]
            rows.append(row)
        return MatrixNode(rows)

    def visitParensExpr(self, ctx: MiniCalcLangParser.ParensExprContext):
        return self.visit(ctx.expr())

    def visitFuncCallExpr(self, ctx: MiniCalcLangParser.FuncCallExprContext):
        func_name = ctx.ID().getText()
        args = [self.visit(expr) for expr in ctx.expr()]
        return FuncCallNode(func_name, args)

    def visitVarExpr(self, ctx: MiniCalcLangParser.VarExprContext):
        return VariableNode(ctx.ID().getText())

    def visitNumberExpr(self, ctx: MiniCalcLangParser.NumberExprContext):
        return NumberNode(float(ctx.NUMBER().getText()))

    def visitStringExpr(self, ctx: MiniCalcLangParser.StringExprContext):
        val = ctx.STRING().getText()[1:-1]
        return StringNode(val)

    def visitBoolExpr(self, ctx: MiniCalcLangParser.BoolExprContext):
        val = True if ctx.getText() == 'true' else False
        return BoolNode(val)

    def visitUnaryExpr(self, ctx: MiniCalcLangParser.UnaryExprContext):
        op = ctx.getChild(0).getText()
        return UnaryOpNode(op, self.visit(ctx.expr()))

    def visitTransposeExpr(self, ctx: MiniCalcLangParser.TransposeExprContext):
        return UnaryOpNode("'", self.visit(ctx.expr()))

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

    def visitBreak_stmt(self, ctx: MiniCalcLangParser.Break_stmtContext):
        return BreakNode()

    def visitContinue_stmt(self, ctx: MiniCalcLangParser.Continue_stmtContext):
        return ContinueNode()