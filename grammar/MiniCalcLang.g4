grammar MiniCalcLang;

// ==========================================
// PARSER (REGUŁY STRUKTURALNE)
// ==========================================

program
    : statement* EOF
    ;

statement
    : def_stmt
    | const_declaration
    | var_declaration
    | assignment
    | compound_assignment
    | print_stmt
    | if_stmt
    | while_stmt
    | for_stmt
    | repeat_until_stmt
    | switch_stmt
    | return_stmt
    | break_stmt
    | continue_stmt 
    | expr_stmt
    ;

block
    : PUNCT_LBRACE statement* PUNCT_RBRACE
    ;

// --- Instrukcje szczegółowe ---
def_stmt
    : KEYWORD_DEF ID PUNCT_LPAREN parameter_list? PUNCT_RPAREN block
    ;

const_declaration
    : KEYWORD_CONST ID PUNCT_ASSIGN literal PUNCT_SEMI
    ;

var_declaration
    : KEYWORD_VAR ID (PUNCT_ASSIGN expr)? PUNCT_SEMI
    ;

parameter_list
    : ID (PUNCT_COMMA ID)*
    ;

assignment
    : ID PUNCT_ASSIGN expr PUNCT_SEMI
    ;

compound_assignment
    : ID (OP_ADD_ASSIGN | OP_SUB_ASSIGN | OP_MUL_ASSIGN | OP_DIV_ASSIGN) expr PUNCT_SEMI
    ;

print_stmt
    : KEYWORD_PRINT PUNCT_LPAREN expression_list? PUNCT_RPAREN PUNCT_SEMI
    ;

expression_list
    : expr (PUNCT_COMMA expr)*
    ;

if_stmt
    : KEYWORD_IF expr block (KEYWORD_ELIF expr block)* (KEYWORD_ELSE block)?
    ;

while_stmt
    : KEYWORD_WHILE expr block
    ;

for_stmt
    : KEYWORD_FOR ID PUNCT_ASSIGN expr KEYWORD_TO expr (KEYWORD_STEP expr)? block
    ;

repeat_until_stmt
    : KEYWORD_REPEAT block KEYWORD_UNTIL expr PUNCT_SEMI
    ;

switch_stmt
    : KEYWORD_SWITCH expr PUNCT_LBRACE case_branch* default_branch? PUNCT_RBRACE
    ;

case_branch
    : KEYWORD_CASE literal PUNCT_COLON statement
    ;

default_branch
    : KEYWORD_DEFAULT PUNCT_COLON statement
    ;

return_stmt
    : KEYWORD_RETURN expr? PUNCT_SEMI
    ;

break_stmt
    : KEYWORD_BREAK PUNCT_SEMI
    ;

continue_stmt
    : KEYWORD_CONTINUE PUNCT_SEMI
    ;

expr_stmt
    : expr PUNCT_SEMI
    ;

// ==========================================
// WYRAŻENIA (Z JAWNYMI ETYKIETAMI)
// ==========================================

expr
    : matrix_expr                                                   # MatrixExpr
    | list_expr                                                     # ListExpr
    | PUNCT_LPAREN expr PUNCT_RPAREN                                # ParensExpr
    | ID PUNCT_LPAREN expression_list? PUNCT_RPAREN                 # FuncCallExpr
    | expr PUNCT_LBRACKET expression_list PUNCT_RBRACKET            # IndexExpr
    | ID                                                            # VarExpr
    | literal                                                       # LiteralExpr
    | expr OP_TRANSPOSE                                             # TransposeExpr
    | (OP_PLUS | OP_MINUS | KEYWORD_NOT) expr                       # UnaryExpr
    | expr OP_POW expr                                              # PowerExpr
    | expr (OP_MUL | OP_DIV | OP_MOD) expr                          # MulDivExpr
    | expr (OP_PLUS | OP_MINUS) expr                                # AddSubExpr
    | expr (OP_GT | OP_LT | OP_GTE | OP_LTE | OP_EQ | OP_NEQ) expr   # RelationalExpr
    | expr KEYWORD_AND expr                                         # AndExpr
    | expr KEYWORD_OR expr                                          # OrExpr
    ;

matrix_expr
    : PUNCT_LBRACKET matrix_row (PUNCT_COMMA matrix_row)* PUNCT_RBRACKET
    ;

matrix_row
    : PUNCT_LBRACKET expr (PUNCT_COMMA expr)* PUNCT_RBRACKET
    ;

list_expr
    : PUNCT_LBRACKET expr (PUNCT_COMMA expr)* PUNCT_RBRACKET
    ;

literal
    : NUMBER
    | STRING
    | KEYWORD_TRUE
    | KEYWORD_FALSE
    | KEYWORD_NULL
    | CONST_PI
    | CONST_E
    ;

// ==========================================
// LEXER (TOKENY)
// ==========================================

// --- Słowa kluczowe ---
KEYWORD_DEF      : 'def';
KEYWORD_RETURN   : 'return';
KEYWORD_IF       : 'if';
KEYWORD_ELIF     : 'elif';
KEYWORD_ELSE     : 'else';
KEYWORD_WHILE    : 'while';
KEYWORD_FOR      : 'for';
KEYWORD_TO       : 'to';
KEYWORD_STEP     : 'step';
KEYWORD_REPEAT   : 'repeat';
KEYWORD_UNTIL    : 'until';
KEYWORD_SWITCH   : 'switch';
KEYWORD_CASE     : 'case';
KEYWORD_DEFAULT  : 'default';
KEYWORD_PRINT    : 'print';
KEYWORD_BREAK    : 'break';
KEYWORD_CONTINUE : 'continue';
KEYWORD_CONST    : 'const';
KEYWORD_VAR      : 'var';

// --- Stałe i wartości logiczne ---
KEYWORD_TRUE     : 'true';
KEYWORD_FALSE    : 'false';
KEYWORD_NULL     : 'null';
CONST_PI         : 'pi';
CONST_E          : 'e';

// --- Operatory logiczne ---
KEYWORD_AND      : 'and';
KEYWORD_OR       : 'or';
KEYWORD_NOT      : 'not';

// --- Operatory arytmetyczne ---
OP_PLUS          : '+';
OP_MINUS         : '-';
OP_MUL           : '*';
OP_DIV           : '/';
OP_MOD           : '%';
OP_POW           : '^';
OP_TRANSPOSE     : '\'';

// --- Przypisania złożone ---
OP_ADD_ASSIGN    : '+=';
OP_SUB_ASSIGN    : '-=';
OP_MUL_ASSIGN    : '*=';
OP_DIV_ASSIGN    : '/=';

// --- Operatory relacyjne ---
OP_GT            : '>';
OP_LT            : '<';
OP_GTE           : '>=';
OP_LTE           : '<=';
OP_EQ            : '==';
OP_NEQ           : '!=';

// --- Znaki interpunkcyjne ---
PUNCT_ASSIGN     : '=';
PUNCT_LPAREN     : '(';
PUNCT_RPAREN     : ')';
PUNCT_LBRACE     : '{';
PUNCT_RBRACE     : '}';
PUNCT_LBRACKET   : '[';
PUNCT_RBRACKET   : ']';
PUNCT_COMMA      : ',';
PUNCT_COLON      : ':';
PUNCT_SEMI       : ';';

// --- Typy podstawowe ---
ID     : [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER : [0-9]+ ('.' [0-9]+)?;
STRING : '"' ~["]* '"';

// --- Białe znaki i komentarze ---
WS      : [ \t\r\n]+ -> skip;
COMMENT : '#' ~[\r\n]* -> skip;