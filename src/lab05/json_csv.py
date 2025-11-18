from pathlib import Path
import json
import csv


def json_to_csv(json_path: str, csv_path: str) -> None:
    json_file = Path(json_path)
    try:
        with json_file.open("r", encoding="utf-8") as j:
            data = json.load(j)
        if not isinstance(data, list) or not all(
            isinstance(item, dict) for item in data
        ):
            raise ValueError("Некорректный формат JSON: ожидается список словарей.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {json_path} не найден.")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка парсинга JSON в файле {json_path}.")

    if not data:
        keys = []
    else:
        keys = set().union(*(d.keys() for d in data))

    with open(csv_path, "w", newline="", encoding="utf-8") as c:
        writer = csv.DictWriter(c, fieldnames=sorted(keys))
        writer.writeheader()
        for entry in data:
            writer.writerow({k: entry.get(k, "") for k in keys})


def csv_to_json(csv_path: str, json_path: str) -> None:
    csv_file = Path(csv_path)
    if not csv_file.is_file():
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    csv_data = []  # пустой список словарей
    with csv_file.open("r", encoding="utf-8") as c:
        reader = csv.DictReader(c)
        for row_num, row in enumerate(reader, start=2):  # start=2: строка 1 — заголовок
            # Проверяем каждое значение
            for key, value in row.items():
                if value is None:
                    raise ValueError(
                        f"Поле '{key}' имеет значение None в строке {row_num}"
                    )
            csv_data.append(row)
    if not csv_data:  # проверка пусто или none
        raise ValueError("Файл пуст или плохо сформирован.")
    with open(json_path, "w", encoding="utf-8") as j:
        json.dump(csv_data, j, ensure_ascii=False, indent=4)
