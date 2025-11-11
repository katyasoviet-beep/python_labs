from pathlib import Path
import json, csv

def json_to_csv(json_path:str, csv_path:str) -> None:
    json_file = Path(json_path)  # объект - файл с путем
    if not json_file.is_file():  # проверка существования файла
        raise FileNotFoundError(f"Файл {json_path} не найден.")
    with json_file.open('r', encoding='utf-8') as j:
        data = json.load(j)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):  # Проверка на формат
        raise ValueError("Ошибка формата")
    keys = set()  # создаём множество ключей
    for element in data: # проходим по всем элементам data
        keys.update(element.keys()) # Получили ключевые слова
        # update - добаляет новые эл-ты в множество   .keys - вытаскивает ключи из элементов
    with open(csv_path, 'w', newline='', encoding='utf-8') as c:
        # открываем файл csv для чтения 'w' newline - обозначает конец строки (при '' отключает преобразование строк)
        writer = csv.DictWriter(c, fieldnames=sorted(keys))  # создаём переменную порядок колонок алфавитный
        writer.writeheader()
        for entry in data:
            # заполняем недостающие элементы
            writer.writerow({key: entry.get(key, '') for key in keys})


def csv_to_json(csv_path: str, json_path: str) -> None:
    csv_file = Path(csv_path) # объект - файл с путем
    if not csv_file.is_file():  # проверка на существование файла
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    csv_data = []  # пустой список словарей
    with csv_file.open('r', encoding='utf-8') as c: # открытие файла в режиме чтения
        reader = csv.DictReader(c)  # читает файл как список словарей
        for row in reader:
            csv_data.append(row)  # добавляем ряд
    if not csv_data:  # проверка пусто или none
        raise ValueError("Файл пуст или плохо сформирован.")
    with open(json_path, 'w', encoding='utf-8') as j: # открытие файла в режиме записи
        json.dump(csv_data, j, ensure_ascii=False, indent=4)  # запись в файл ensure_ascii=False - запрет на показ не нужных символах

# Тест
csv_to_json('data/samples/people.csv', 'data/out/people_from_csv.json')
json_to_csv('data/samples/people.json', 'data/out/people_from_json.csv')