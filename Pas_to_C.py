#!/usr/bin/env python3
"""
Точка входа для транслятора Pascal → C++

Запуск:
    python run_translator.py program.pas
    python run_translator.py program.pas -o output.cpp
    python run_translator.py program.pas -v
"""

from src.translator import main

if __name__ == '__main__':
    main()