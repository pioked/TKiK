# Interpreter MiniCalcLang

## 1. Temat projektu
**MiniCalcLang** – interpreter języka programowania przeznaczonego do obliczeń naukowych, algebry liniowej (macierzy) oraz instrukcji sterujących przepływem.

## 2. Dane studenta
* **Imię i nazwisko:** Piotr Kędziora
* **E-mail:** pkedziora@student.agh.edu.pl

## 3. Założenia programu

### Ogólne cele programu
Celem projektu jest stworzenie języka ułatwiającego przeprowadzanie obliczeń matematycznych i macierzowych. Język umożliwia definiowanie zmiennych, tworzenie własnych funkcji, kontrolowanie przepływu programu (pętle `while`, `for`, instrukcje `if/else`) oraz natywną obsługę operacji na macierzach (mnożenie, transpozycja). 

### Rodzaj translatora
**Interpreter** oparty o Drzewo Składni Abstrakcyjnej (AST). Program nie kompiluje kodu źródłowego do kodu maszynowego ani bajtkodu. Zamiast tego buduje wewnętrzną reprezentację (AST) i wykonuje ją węzeł po węźle z wykorzystaniem wzorca projektowego *Visitor* oraz własnego środowiska pamięci (*Scope/Environment*).

### Wynik działania programu
Program wczytuje kod źródłowy z pliku tekstowego (`.mcl`), analizuje go, rozwiązuje wyrażenia matematyczne i logiczne, a na podstawie instrukcji `print` wyświetla przetworzone wyniki na standardowym wyjściu (np. wynik mnożenia macierzy w formacie tekstowym). W przypadku błędów składniowych lub semantycznych zgłasza precyzyjne wyjątki wraz z numerem linii.

### Planowany język implementacji
* **Język:** Python 3.12+

### Sposób realizacji skanera i parsera
Skaner (lexer) oraz parser zostały wygenerowane automatycznie przy użyciu generatora **ANTLR4** z docelowym językiem generacji (target) ustawionym na Pythona. Następnie, wygenerowane drzewo składniowe (Parse Tree) jest mapowane na autorskie klasy AST, oddzielając gramatykę od logiki wykonawczej interpretera.

---

## 4. Opis tokenów

Poniższa tabela przedstawia zestawienie wszystkich tokenów używanych przez analizator leksykalny w języku MiniCalcLang.

| Kategoria | Nazwa Tokenu | Wyrażenie regularne / Tekst | Opis |
| :--- | :--- | :--- | :--- |
| **Słowa kluczowe** | `KEYWORD_DEF` | `'def'` | Deklaracja nowej funkcji |
| | `KEYWORD_RETURN` | `'return'` | Instrukcja powrotu / zwrócenia wartości |
| | `KEYWORD_IF` | `'if'` | Instrukcja warunkowa |
| | `KEYWORD_ELIF` | `'elif'` | Kolejny warunek w strukturze IF |
| | `KEYWORD_ELSE` | `'else'` | Blok alternatywny instrukcji warunkowej |
| | `KEYWORD_WHILE` | `'while'` | Pętla dopóki warunek spełniony |
| | `KEYWORD_FOR` | `'for'` | Pętla iteracyjna o znanym zakresie |
| | `KEYWORD_TO` | `'to'` | Zakres końcowy pętli FOR |
| | `KEYWORD_STEP` | `'step'` | Krok inkrementacji pętli FOR |
| | `KEYWORD_REPEAT` | `'repeat'` | Początek pętli do-while (wykonaj... dopóki) |
| | `KEYWORD_UNTIL` | `'until'` | Warunek zakończenia pętli REPEAT |
| | `KEYWORD_SWITCH` | `'switch'` | Instrukcja wyboru wielowariantowego |
| | `KEYWORD_CASE` | `'case'` | Wariant wartości w instrukcji SWITCH |
| | `KEYWORD_DEFAULT` | `'default'` | Opcja domyślna w strukturze SWITCH |
| | `KEYWORD_PRINT` | `'print'` | Funkcja systemowa wypisania tekstu |
| | `KEYWORD_BREAK` | `'break'` | Natychmiastowe przerwanie pętli |
| | `KEYWORD_CONTINUE`| `'continue'` | Przejście do kolejnej iteracji pętli |
| | `KEYWORD_CONST` | `'const'` | Deklaracja stałej globalnej |
| | `KEYWORD_VAR` | `'var'` | Deklaracja zmiennej |
| **Wartości wbudowane**| `KEYWORD_TRUE` | `'true'` | Wartość logiczna prawdy |
| | `KEYWORD_FALSE` | `'false'` | Wartość logiczna fałszu |
| | `KEYWORD_NULL` | `'null'` | Reprezentacja pustej wartości |
| | `CONST_PI` | `'pi'` | Matematyczna stała pi (3.14159) |
| | `CONST_E` | `'e'` | Stała Eulera (2.71828) |
| **Operatory logiczne**| `KEYWORD_AND` | `'and'` | Koniunkcja logiczna |
| | `KEYWORD_OR` | `'or'` | Alternatywa logiczna |
| | `KEYWORD_NOT` | `'not'` | Negacja unarna logiczna |
| **Operatory arytm.** | `OP_PLUS` | `'+'` | Dodawanie / plus unarny |
| | `OP_MINUS` | `'-'` | Odejmowanie / minus unarny |
| | `OP_MUL` | `'*'` | Mnożenie (w tym macierzowe) |
| | `OP_DIV` | `'/'` | Dzielenie standardowe |
| | `OP_MOD` | `'%'` | Operacja modulo (reszta z dzielenia) |
| | `OP_POW` | `'^'` | Potęgowanie |
| | `OP_TRANSPOSE` | `'''` | Operator transpozycji macierzy |
| **Skróty przypisania**| `OP_ADD_ASSIGN` | `'+='` | Przypisanie z dodawaniem |
| | `OP_SUB_ASSIGN` | `'-='` | Przypisanie z odejmowaniem |
| | `OP_MUL_ASSIGN` | `'*='` | Przypisanie z mnożeniem |
| | `OP_DIV_ASSIGN` | `'/='` | Przypisanie z dzieleniem |
| **Operatory relacyjne**| `OP_GT` | `'>'` | Większe niż |
| | `OP_LT` | `'<'` | Mniejsze niż |
| | `OP_GTE` | `'>='` | Większe bądź równe |
| | `OP_LTE` | `'<='` | Mniejsze bądź równe |
| | `OP_EQ` | `'=='` | Porównanie strukturalne równości |
| | `OP_NEQ` | `'!='` | Porównanie strukturalne nierówności |
| **Interpunkcja** | `PUNCT_ASSIGN` | `'='` | Standardowy operator przypisania |
| | `PUNCT_LPAREN` | `'('` | Otwarcie bloku argumentów / nawiasów |
| | `PUNCT_RPAREN` | `')'` | Zamknięcie bloku argumentów / nawiasów |
| | `PUNCT_LBRACE` | `'{'` | Rozpoczęcie bloku kodu lokalnego |
| | `PUNCT_RBRACE` | `'}'` | Zakończenie bloku kodu lokalnego |
| | `PUNCT_LBRACKET` | `'['` | Otwarcie deklaracji tablicy/macierzy/indeksu |
| | `PUNCT_RBRACKET` | `']'` | Zamknięcie deklaracji tablicy/macierzy/indeksu |
| | `PUNCT_COMMA` | `','` | Separator elementów list / argumentów |
| | `PUNCT_COLON` | `':'` | Separator etykiet struktur sterujących |
| | `PUNCT_SEMI` | `';'` | Znak zakończenia instrukcji |
| **Dane bazowe** | `ID` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy własne zmiennych i funkcji |
| | `NUMBER` | `[0-9]+ ('.' [0-9]+)?`| Literały liczbowe |
| | `STRING` | `'"' ~["]* '"'` | Łańcuchy tekstowe w cudzysłowach |
| **Niewidoczne** | `WS` | `[ \t\r\n]+` | Białe znaki (pomijane) |
| | `COMMENT` | `'#' ~[\r\n]*` | Komentarze jednoliniowe (pomijane) |

---

## 5. Gramatyka formatu (Notacja ANTLR4)

Poniżej znajduje się pełna formalna gramatyka języka (bez akcji semantycznych), definiująca reguły produkcyjne parsera. Warto zauważyć, że priorytety operatorów są zdefiniowane przez kolejność reguł w produkcie `expr`.

```antlr
grammar MiniCalcLang;

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