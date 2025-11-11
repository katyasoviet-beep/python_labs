import argparse
import sys  
from pathlib import Path
from src.lab03.text import count_freq, top_n, tokenize


def main():
    parser = argparse.ArgumentParser(
        prog="text-cli",
        description="Утилита для просмотра и анализа текстовых файлов",
        epilog="""
Примеры:
  text-cli cat --input data.txt
  text-cli cat --input data.txt -n
  text-cli stats --input data.txt --top 10
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Подкоманда: cat
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла построчно")
    cat_parser.add_argument("--input", "-i", type=Path, required=True, help="Путь к входному текстовому файлу")
    cat_parser.add_argument("-n", action="store_true", help="Добавить нумерацию строк")

    # Подкоманда: stats
    stats_parser = subparsers.add_parser("stats", help="Показать частоту слов в тексте")
    stats_parser.add_argument("--input", "-i", type=Path, required=True, help="Путь к файлу для анализа")
    stats_parser.add_argument("--top", "-t", type=int, default=5, help="Количество самых частотных слов (по умолчанию: 5)")

    args = parser.parse_args()

    # Проверка: команда обязательна
    if not args.command:
        parser.print_help()
        sys.exit(1)

    input_path = args.input

    try:
        if args.command == "cat":
            with input_path.open(mode='r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    line = line.rstrip('\n\r')
                    if args.n:
                        print(f"{line_num}  {line}")
                    else:
                        print(line)

        elif args.command == "stats":
            with input_path.open(mode='r', encoding='utf-8') as f:
                text = f.read()
                tokens = tokenize(text)
            freq = count_freq(tokens)
            top_words = top_n(freq, args.top)
            for word, count in top_words:
                print(f"{word}: {count}")

        else:
            parser.print_help()
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ Ошибка: файл не найден — '{input_path}'", file=sys.stderr)
        sys.exit(1)

    except PermissionError:
        print(f"❌ Ошибка: нет прав на чтение файла — '{input_path}'", file=sys.stderr)
        sys.exit(1)

    except IsADirectoryError:
        print(f"❌ Ошибка: указан путь к папке, а не к файлу — '{input_path}'", file=sys.stderr)
        sys.exit(1)

    except UnicodeDecodeError:
        print(f"❌ Ошибка: файл '{input_path}' не может быть прочитан как текст в кодировке UTF-8.", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()  
