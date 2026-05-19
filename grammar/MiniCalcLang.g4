grammar MiniCalcLang;

// --- REGUŁY GŁÓWNE ---
program: statement* EOF;

statement:
      def_stmt
    | assignment
    | print_stmt
    | if_stmt
    | while_stmt
    | for_stmt
    | return_stmt
    | break_stmt
    | continue_stmt 
    | expr_stmt
    ;

block: '{' statement* '}';

def_stmt: 'def' ID '(' (ID (',' ID)*)? ')' block;
assignment: ID '=' expr;
print_stmt: 'print' '(' expr ')';
if_stmt: 'if' expr block ('else' block)?;
while_stmt: 'while' expr block;
for_stmt: 'for' ID '=' expr 'to' expr ('step' expr)? block;
return_stmt: 'return' expr?;
break_stmt: 'break';
continue_stmt: 'continue';
expr_stmt: expr;

// --- WYRAŻENIA (Z PRIORYTETAMI) ---
expr:
      matrix_expr                                       # MatrixExpr
    | '(' expr ')'                                      # ParensExpr
    | ID '(' (expr (',' expr)*)? ')'                    # FuncCallExpr
    | ID                                                # VarExpr
    | NUMBER                                            # NumberExpr
    | STRING                                            # StringExpr
    | TRUE | FALSE                                      # BoolExpr
    | expr '\''                                         # TransposeExpr
    | ('+' | '-' | 'not') expr                          # UnaryExpr (Dodano '+')
    | expr '^' expr                                     # PowerExpr
    | expr ('*' | '/' | '%') expr                       # MulDivExpr
    | expr ('+' | '-') expr                             # AddSubExpr
    | expr ('>' | '<' | '>=' | '<=' | '==' | '!=') expr # RelationalExpr
    | expr 'and' expr                                   # AndExpr
    | expr 'or' expr                                    # OrExpr
    ;

matrix_expr: '[' matrix_row (',' matrix_row)* ']';
matrix_row: '[' expr (',' expr)* ']';

// --- TOKENY ---
TRUE: 'true';
FALSE: 'false';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' ~["]* '"';

WS: [ \t\r\n]+ -> skip;
COMMENT: '#' ~[\r\n]* -> skip;