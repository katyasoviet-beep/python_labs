import argparse
import sys  
from pathlib import Path
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def main():
    parser = argparse.ArgumentParser(
        prog="data-converter",
        description="Утилита для конвертации данных между форматами: JSON, CSV, XLSX",
        epilog="""
Примеры:
  data-converter json2csv --in data.json --out data.csv
  data-converter csv2json --in data.csv --out data.json
  data-converter csv2xlsx --in data.csv --out data.xlsx
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    sub = parser.add_subparsers(dest="cmd", help="Доступные команды конвертации")

    # Команда: json2csv
    p1 = sub.add_parser("json2csv", help="Конвертировать JSON в CSV")
    p1.add_argument("--in", "-i", dest="input", type=Path, required=True, help="Входной JSON-файл")
    p1.add_argument("--out", "-o", dest="output", type=Path, required=True, help="Выходной CSV-файл")

    # Команда: csv2json
    p2 = sub.add_parser("csv2json", help="Конвертировать CSV в JSON")
    p2.add_argument("--in", "-i", dest="input", type=Path, required=True, help="Входной CSV-файл")
    p2.add_argument("--out", "-o", dest="output", type=Path, required=True, help="Выходной JSON-файл")

    # Команда: csv2xlsx
    p3 = sub.add_parser("csv2xlsx", help="Конвертировать CSV в XLSX")
    p3.add_argument("--in", "-i", dest="input", type=Path, required=True, help="Входной CSV-файл")
    p3.add_argument("--out", "-o", dest="output", type=Path, required=True, help="Выходной XLSX-файл")

    args = parser.parse_args()

    # Проверка: команда обязательна
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    # Конвертация
    try:
        input_file = args.input
        output_file = args.output

        if args.cmd == "json2csv":
            json_to_csv(input_file, output_file)
            print(f"✅ Успешно сохранено: {output_file}")
        elif args.cmd == "csv2json":
            csv_to_json(input_file, output_file)
            print(f"✅ Успешно сохранено: {output_file}")
        elif args.cmd == "csv2xlsx":
            csv_to_xlsx(input_file, output_file)
            print(f"✅ Успешно сохранено: {output_file}")
        else:
            parser.print_help()
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ Ошибка: входной файл не найден — '{input_file}'", file=sys.stderr)
        sys.exit(1)

    except IsADirectoryError:
        print(f"❌ Ошибка: путь '{input_file}' — это папка, а не файл", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"❌ Ошибка доступа: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка при конвертации: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()  
