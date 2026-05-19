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
| **Słowa kluczowe** | `DEF` | `'def'` | Deklaracja funkcji |
| | `RETURN` | `'return'` | Zwracanie wartości z funkcji |
| | `IF` | `'if'` | Instrukcja warunkowa |
| | `ELSE` | `'else'` | Alternatywa instrukcji warunkowej |
| | `WHILE` | `'while'` | Pętla warunkowa |
| | `FOR` | `'for'` | Pętla iteracyjna |
| | `TO` | `'to'` | Słowo kluczowe pętli for (zakres) |
| | `STEP` | `'step'` | Opcjonalny krok w pętli for |
| | `PRINT` | `'print'` | Instrukcja wypisania na ekran |
| **Stałe logiczne** | `TRUE` | `'true'` | Wartość logiczna Prawda |
| | `FALSE` | `'false'` | Wartość logiczna Fałsz |
| **Operatory logiczne** | `AND` | `'and'` | Koniunkcja logiczna |
| | `OR` | `'or'` | Alternatywa logiczna |
| | `NOT` | `'not'` | Negacja logiczna |
| **Operatory arytmet.**| `PLUS` | `'+'` | Dodawanie |
| | `MINUS` | `'-'` | Odejmowanie / Negacja unarna |
| | `MUL` | `'*'` | Mnożenie |
| | `DIV` | `'/'` | Dzielenie |
| | `MOD` | `'%'` | Reszta z dzielenia (Modulo) |
| | `POW` | `'^'` | Potęgowanie |
| | `TRANSPOSE` | `'''` (apostrof) | Transpozycja macierzy |
| **Operatory relacyjne**| `GT` | `'>'` | Większe niż |
| | `LT` | `'<'` | Mniejsze niż |
| | `GTE` | `'>='` | Większe lub równe |
| | `LTE` | `'<='` | Mniejsze lub równe |
| | `EQ` | `'=='` | Równe |
| | `NEQ` | `'!='` | Różne |
| **Znaki strukturalne** | `ASSIGN` | `'='` | Przypisanie |
| | `LPAREN` | `'('` | Otwarcie nawiasu okrągłego |
| | `RPAREN` | `')'` | Zamknięcie nawiasu okrągłego |
| | `LBRACE` | `'{'` | Otwarcie bloku kodu |
| | `RBRACE` | `'}'` | Zamknięcie bloku kodu |
| | `LBRACKET` | `'['` | Otwarcie nawiasu kwadratowego |
| | `RBRACKET` | `']'` | Zamknięcie nawiasu kwadratowego |
| | `COMMA` | `','` | Przecinek / separator |
| **Typy danych** | `ID` | `[a-zA-Z_][a-zA-Z0-9_]*` | Identyfikator (zmienna/funkcja) |
| | `NUMBER` | `[0-9]+ ('.' [0-9]+)?` | Liczba całkowita / zmiennoprzecinkowa |
| | `STRING` | `'"' ~["]* '"'` | Ciąg znaków (napis) |
| **Białe znaki** | `WS` | `[ \t\r\n]+` | Ignorowane znaki (-> skip) |
| | `COMMENT` | `'#' ~[\r\n]*` | Komentarze jednolinijkowe (-> skip) |

---

## 5. Gramatyka formatu (Notacja ANTLR4)

Poniżej znajduje się pełna formalna gramatyka języka (bez akcji semantycznych), definiująca reguły produkcyjne parsera. Warto zauważyć, że priorytety operatorów są zdefiniowane przez kolejność reguł w produkcie `expr`.

```antlr
rammar MiniCalcLang;

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

expr:
      matrix_expr                                       
    | '(' expr ')'                                  
    | ID '(' (expr (',' expr)*)? ')'                   
    | ID                                           
    | NUMBER                                           
    | STRING                                            
    | (TRUE | FALSE)                               
    | expr '\''                                   
    | ('+' | '-' | 'not') expr                      
    | expr '^' expr                        
    | expr ('*' | '/' | '%') expr                  
    | expr ('+' | '-') expr                             
    | expr ('>' | '<' | '>=' | '<=' | '==' | '!=') expr 
    | expr 'and' expr                                  
    | expr 'or' expr                                   
    ;

matrix_expr: '[' matrix_row (',' matrix_row)* ']';
matrix_row: '[' expr (',' expr)* ']';

TRUE: 'true';
FALSE: 'false';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' ~["]* '"';

WS: [ \t\r\n]+;
COMMENT: '#' ~[\r\n]*;