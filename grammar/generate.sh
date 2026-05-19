#!/bin/bash

echo "Generowanie Lexera i Parsera ANTLR4 dla języka Python3..."
mkdir -p ../src/parser/generated
antlr4 -Dlanguage=Python3 -visitor -no-listener MiniCalcLang.g4 -o ../src/parser/generated
echo "Generacja zakończona sukcesem!"