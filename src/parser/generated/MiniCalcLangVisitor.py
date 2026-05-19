# Generated from MiniCalcLang.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MiniCalcLangParser import MiniCalcLangParser
else:
    from MiniCalcLangParser import MiniCalcLangParser

# This class defines a complete generic visitor for a parse tree produced by MiniCalcLangParser.

class MiniCalcLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniCalcLangParser#program.
    def visitProgram(self, ctx:MiniCalcLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#statement.
    def visitStatement(self, ctx:MiniCalcLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#block.
    def visitBlock(self, ctx:MiniCalcLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#def_stmt.
    def visitDef_stmt(self, ctx:MiniCalcLangParser.Def_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#assignment.
    def visitAssignment(self, ctx:MiniCalcLangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#print_stmt.
    def visitPrint_stmt(self, ctx:MiniCalcLangParser.Print_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#if_stmt.
    def visitIf_stmt(self, ctx:MiniCalcLangParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#while_stmt.
    def visitWhile_stmt(self, ctx:MiniCalcLangParser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#for_stmt.
    def visitFor_stmt(self, ctx:MiniCalcLangParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#return_stmt.
    def visitReturn_stmt(self, ctx:MiniCalcLangParser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#break_stmt.
    def visitBreak_stmt(self, ctx:MiniCalcLangParser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#continue_stmt.
    def visitContinue_stmt(self, ctx:MiniCalcLangParser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#expr_stmt.
    def visitExpr_stmt(self, ctx:MiniCalcLangParser.Expr_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#AndExpr.
    def visitAndExpr(self, ctx:MiniCalcLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#StringExpr.
    def visitStringExpr(self, ctx:MiniCalcLangParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#BoolExpr.
    def visitBoolExpr(self, ctx:MiniCalcLangParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#MatrixExpr.
    def visitMatrixExpr(self, ctx:MiniCalcLangParser.MatrixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#RelationalExpr.
    def visitRelationalExpr(self, ctx:MiniCalcLangParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:MiniCalcLangParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#OrExpr.
    def visitOrExpr(self, ctx:MiniCalcLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#PowerExpr.
    def visitPowerExpr(self, ctx:MiniCalcLangParser.PowerExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:MiniCalcLangParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#NumberExpr.
    def visitNumberExpr(self, ctx:MiniCalcLangParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#ParensExpr.
    def visitParensExpr(self, ctx:MiniCalcLangParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#VarExpr.
    def visitVarExpr(self, ctx:MiniCalcLangParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:MiniCalcLangParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#TransposeExpr.
    def visitTransposeExpr(self, ctx:MiniCalcLangParser.TransposeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#FuncCallExpr.
    def visitFuncCallExpr(self, ctx:MiniCalcLangParser.FuncCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#matrix_expr.
    def visitMatrix_expr(self, ctx:MiniCalcLangParser.Matrix_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCalcLangParser#matrix_row.
    def visitMatrix_row(self, ctx:MiniCalcLangParser.Matrix_rowContext):
        return self.visitChildren(ctx)



del MiniCalcLangParser