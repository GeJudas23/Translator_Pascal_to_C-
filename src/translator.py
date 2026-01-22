"""
Главное приложение транслятора Pascal → C++
Интерфейс командной строки
"""

import sys
import argparse
from pathlib import Path
from src.lexer import Lexer, LexerError
from src.parser import Parser, ParserError
from src.codegen import CodeGenerator

# Установка UTF-8 кодировки для консоли на Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def translate_file(input_path: str, output_path: str = None, verbose: bool = False):
    """
    Транслирует файл Pascal в C++
    
    Args:
        input_path: Путь к входному файлу Pascal
        output_path: Путь к выходному файлу C++ (необязательно)
        verbose: Выводить подробную информацию
    """
    try:
        # Чтение исходного файла
        with open(input_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        if verbose:
            print(f"Чтение файла: {input_path}")
            print(f"Размер исходного кода: {len(source)} символов\n")
        
        # Лексический анализ
        if verbose:
            print("=" * 60)
            print("ЭТАП 1: Лексический анализ")
            print("=" * 60)
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if verbose:
            print(f"Найдено токенов: {len(tokens)}")
            print("\nПервые 20 токенов:")
            for token in tokens[:20]:
                print(f"  {token}")
            print()
        
        # Синтаксический анализ
        if verbose:
            print("=" * 60)
            print("ЭТАП 2: Синтаксический анализ")
            print("=" * 60)
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        if verbose:
            print(f"Программа: {ast.name}")
            print(f"Переменных: {len(ast.variables)}")
            print(f"Подпрограмм: {len(ast.subprograms)}")
            print()
        
        # Генерация кода C++
        if verbose:
            print("=" * 60)
            print("ЭТАП 3: Генерация кода C++")
            print("=" * 60)
        
        generator = CodeGenerator()
        cpp_code = generator.generate(ast)
        
        if verbose:
            print(f"Сгенерировано строк кода: {len(cpp_code.splitlines())}")
            print()
        
        # Определение выходного файла
        if output_path is None:
            input_file = Path(input_path)
            output_path = input_file.with_suffix('.cpp')
        
        # Запись результата
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cpp_code)
        
        print("=" * 60)
        print(f"✓ Трансляция успешно завершена!")
        print(f"  Входной файл:  {input_path}")
        print(f"  Выходной файл: {output_path}")
        print("=" * 60)
        
        if verbose:
            print("\nСгенерированный код C++:")
            print("-" * 60)
            print(cpp_code)
            print("-" * 60)
        
        return True
    
    except FileNotFoundError:
        print(f"✗ Ошибка: Файл '{input_path}' не найден", file=sys.stderr)
        return False
    
    except LexerError as e:
        print(f"✗ Лексическая ошибка: {e}", file=sys.stderr)
        return False
    
    except ParserError as e:
        print(f"✗ Синтаксическая ошибка: {e}", file=sys.stderr)
        return False
    
    except Exception as e:
        print(f"✗ Неожиданная ошибка: {e}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Транслятор Pascal → C++',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python run_translator.py program.pas                    # Создаст program.cpp
  python run_translator.py program.pas -o output.cpp      # Указать имя выходного файла
  python run_translator.py program.pas -v                 # Подробный вывод
  python run_translator.py program.pas -v -o result.cpp   # Все опции вместе
        """
    )
    
    parser.add_argument('input', help='Входной файл Pascal (.pas)')
    parser.add_argument('-o', '--output', help='Выходной файл C++ (.cpp)')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Подробный вывод процесса трансляции')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()
    
    success = translate_file(args.input, args.output, args.verbose)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()