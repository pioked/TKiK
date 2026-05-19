# Projekt: MiniCalcLang - Interpreter Języka Obliczeń Naukowych

**Przedmiot:** Teoria Kompilacji i Kompilatorów (TKiK)

**Autor:** Piotr Kędziora

**E-mail:** pkedziora@student.agh.edu.pl

## 1. Temat Projektu
MiniCalcLang to autorski, interpretowany język programowania przeznaczony do obliczeń matematycznych, operacji na macierzach i przeprowadzania prostych symulacji naukowych. 

## 2. Cele programu
Stworzenie w pełni funkcjonalnego interpretera demonstrującego proces kompilacji w locie. Projekt ma edukacyjnie obrazować fazy analizy leksykalnej, parsowania kodu, generacji Drzewa Składni Abstrakcyjnej (AST) oraz wizytowania go w środowisku uruchomieniowym z obsługą pamięci lokalnej (Scope).

## 3. Rodzaj translatora
Bezpośredni interpreter oparty na Drzewie Składni Abstrakcyjnej (AST-walking interpreter). Nie generuje kodu maszynowego ani bajtkodu (nie jest kompilatorem).

## 4. Planowany wynik działania
Wynikiem działania programu są obliczenia i komunikaty zlecane w instrukcjach języka (np. polecenie `print`), wyświetlane na standardowym wyjściu (stdout). Program informuje o błędach składniowych oraz semantycznych (np. nieistniejąca zmienna, niezgodne wymiary macierzy).

## 5. Opis języka
MiniCalcLang to język o składni zbliżonej do Pythona/C, silnie typowany dynamicznie. Zapewnia natywną składnię dla typów liczbowych i macierzy. Obsługuje instrukcje warunkowe, pętle oraz zestaw standardowych funkcji naukowych.

## 6. Opis interpretera
Interpreter bazuje na wzorcu konstrukcyjnym Visitor. Kod po przekształceniu w AST jest obiegany węzeł po węźle, gdzie każda operacja jest realizowana przy użyciu wbudowanego w Python silnika obliczeniowego oraz biblioteki `numpy`. Interpreter posiada własną instancję wirtualnego środowiska (`Environment`), przechowującą zadeklarowane zmienne.

## 7. Język implementacji
* Python 3.12
* Zalecane utworzenie wirtualnego środowiska (venv).

## 8. Opis parsera i skanera
* **Generator:** ANTLR4
* Skaner dzieli strumień wejściowy na tokeny ignorując białe znaki i komentarze.
* Parser buduje drzewo błędu (CST - Concrete Syntax Tree), które za pomocą wzorca Visitor mapowane jest do dedykowanego w Pythonie AST (Abstract Syntax Tree). 

## 9. Opis tokenów
Główne tokeny (terminale) użyte w systemie to:
* `ID`: Zmienne i nazwy funkcji, ciągi znaków alfanumerycznych, zaczynające się od litery.
* `NUMBER`: Liczby całkowite i zmiennoprzecinkowe (np. `42`, `3.14`).
* `WS`, `COMMENT`: Ignorowane znaki sterujące i komentarze jednolinijkowe zaczynające się od `#`.
* Słowa kluczowe: `if`, `while`, `print`.

## 10. Formalna Gramatyka (BNF)
```bnf
<program> ::= <statement>* EOF
<statement> ::= <assignment> | <print_stmt> | <if_stmt> | <while_stmt> | <expr_stmt>
<assignment> ::= ID "=" <expr>
<print_stmt> ::= "print" "(" <expr> ")"
<if_stmt> ::= "if" <expr> "{" <statement>* "}"
<while_stmt> ::= "while" <expr> "{" <statement>* "}"
<expr_stmt> ::= <expr>

<expr> ::= <matrix_expr>
         | "(" <expr> ")"
         | ID "(" [<expr> ("," <expr>)*] ")"
         | ID
         | NUMBER
         | "-" <expr>
         | <expr> "^" <expr>
         | <expr> ("*" | "/" | "%") <expr>
         | <expr> ("+" | "-") <expr>
         | <expr> (">" | "<" | ">=" | "<=" | "==" | "!=") <expr>

<matrix_expr> ::= "[" <matrix_row> ("," <matrix_row>)* "]"
<matrix_row> ::= "[" <expr> ("," <expr>)* "]"
```
## 11. Informacje o bibliotekach
* `antlr4-python3-runtime`: Runtime dla wygenerowanego kodu parsera.
* `numpy`: Realizacja wysoce wydajnych operacji na macierzach.
* `pytest`: Biblioteka testów jednostkowych.
* `math`: Wbudowane wsparcie operacji na liczbach.

## 12. Instrukcja uruchomienia
1. Instalacja zależności: `pip install -r requirements.txt`
2. Generacja parsera: `cd grammar && ./generate.sh`
3. Uruchomienie skryptu: `python src/main.py examples/01_math.mcl`

## 13. Przykłady użycia
```python
# Inicjalizacja macierzy i operacje
A = [[1, 2], [3, 4]]
B = [[2, 0], [1, 2]]
C = A * B
print(C)

# Użycie funkcji i pętli
x = 0
while x < 5 {
    print(sin(x))
    x = x + 1
}