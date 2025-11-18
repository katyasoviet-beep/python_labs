# ЛР7 — Тестирование: pytest + стиль (black)

> **Цель:** научиться писать модульные тесты на `pytest`, измерять покрытие и поддерживать единый стиль кода (`black`).  
> **Связь:** тестируем функции из `src/lib/text.py` (ЛР3) и `src/lab05/json_csv.py` (ЛР5).

---

## Структура
- Код:*[Задание A](test_texts.py/)*
      *[Задание B](test_json_csv.py/)*
- Скриншоты: `images/lab07/`

---

## Задание A — модуль `tests/test_texts.py`
**Файл:** `test_texts.py`  
### Код:
```
import pytest
from lib.texts import normalize, tokenize, count_freq, top_n


# === Тесты для normalize ===


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка!", "ежик, елка!"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),
        ("   \n\t\r   ", ""),
        ("Тест-слово", "тест-слово"),
        ("С-слово и_ещё_одно", "с-слово и_еще_одно"),
    ],
)
def test_normalize_basic(source, expected):
    assert normalize(source) == expected


def test_normalize_casefold_off():
    text = "Привет МИР"
    expected = "Привет МИР"  # не меняется
    assert normalize(text, casefold=False) == expected


def test_normalize_yo2e_off():
    text = "Ёжик и елка"
    expected = "ёжик и елка"  # "Ё" не заменяется
    assert normalize(text, yo2e=False) == expected


# === Тесты для tokenize ===


@pytest.mark.parametrize(
    "text, expected",
    [
        ("привет, мир!", ["привет", "мир"]),
        ("слово-через-дефис", ["слово-через-дефис"]),
        ("слово -не -через", ["слово", "не", "через"]),
        ("", []),
        ("   ", []),
        ("a1b2_3", ["a1b2_3"]),
        ("test123_word", ["test123_word"]),
        ("слово, ещё!", ["слово", "ещё"]),
        ("слово- и ещё", ["слово", "и", "ещё"]),
        ("a-b-c", ["a-b-c"]),
        ("a--b", ["a", "b"]),  # два дефиса — разрывает слово
    ],
)
def test_tokenize_basic(text, expected):
    assert tokenize(text) == expected


# === Тесты для count_freq ===


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([], {}),
        (["a"], {"a": 1}),
        (["a", "b", "a"], {"a": 2, "b": 1}),
        (["один", "два", "один", "два", "один"], {"один": 3, "два": 2}),
    ],
)
def test_count_freq_basic(tokens, expected):
    assert count_freq(tokens) == expected


# === Тесты для top_n ===


def test_top_n_basic():
    freq = {"a": 5, "b": 3, "c": 7}
    result = top_n(freq, 2)
    expected = [("c", 7), ("a", 5)]
    assert result == expected


def test_top_n_n_larger_than_data():
    freq = {"a": 1, "b": 1}
    result = top_n(freq, 5)  # запрашиваем больше, чем есть
    expected = [("a", 1), ("b", 1)]  # всё возвращается
    assert result == expected


def test_top_n_tie_breaker():
    freq = {"банан": 3, "апельсин": 3, "яблоко": 3}
    result = top_n(freq, 3)
    # При равной частоте сортируем по алфавиту
    expected = [("апельсин", 3), ("банан", 3), ("яблоко", 3)]
    assert result == expected


def test_top_n_empty():
    assert top_n({}, 5) == []


def test_top_n_zero():
    freq = {"a": 2, "b": 1}
    assert top_n(freq, 0) == []


# === Интеграционный тест: полная цепочка ===


def test_full_pipeline():
    text = "Привет, ёжик! Привет, мир! Мир — красив."
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, 3)

    # Ожидаем: "привет" (2), "мир" (2), "ёжик|ежик" → "ежик", "красив" (1)
    # После нормализации: "ежик", "привет", "мир", "красив"
    assert freq["привет"] == 2
    assert freq["мир"] == 2
    assert "ежик" in freq
    assert top[0][0] in ["мир", "привет"]  # один из них на первом месте
    assert len(top) == 3
```

---

## Задание B — модуль `tests/test_json_csv.py`
**Файл:** `test_json_csv.py`  
### Код:
```
import csv
import json
from pathlib import Path
import pytest

from lab05.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"
    data = [
        {"name": "Alice", "age": 22, "city": "Moscow"},
        {"name": "Bob", "age": 25, "city": "SPb"},
    ]
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    json_to_csv(str(src), str(dst))

    with open(dst, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert {"name", "age", "city"} <= set(rows[0].keys())
    assert rows[0]["name"] == "Alice"
    assert rows[1]["name"] == "Bob"


def test_csv_to_json_roundtrip(tmp_path: Path):
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"

    with open(src, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerow({"name": "Alice", "age": "22", "city": "Moscow"})
        writer.writerow({"name": "Bob", "age": "25", "city": "SPb"})

    csv_to_json(str(src), str(dst))

    result = json.loads(dst.read_text(encoding="utf-8"))

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == "22"
    assert result[1]["name"] == "Bob"
    assert result[1]["age"] == "25"


def test_json_to_csv_empty_file(tmp_path: Path):
    src = tmp_path / "empty.json"
    dst = tmp_path / "empty.csv"
    src.write_text("[]", encoding="utf-8")

    json_to_csv(str(src), str(dst))

    with open(dst, encoding="utf-8") as f:
        content = f.read().strip()

    assert content == ""


def test_json_to_csv_nonexistent_input(tmp_path: Path):
    src = tmp_path / "nonexistent.json"
    dst = tmp_path / "output.csv"

    with pytest.raises(FileNotFoundError):
        json_to_csv(str(src), str(dst))


def test_json_to_csv_invalid_format(tmp_path: Path):
    # Создаём JSON, который НЕ является списком словарей
    src = tmp_path / "invalid.json"
    dst = tmp_path / "output.csv"

    # Примеры "неправильных" JSON
    invalid_cases = [
        '"just a string"',  # строка
        "123",  # число
        '{"name": "Alice"}',  # объект (словарь), а не список
        "null",  # null
        '{"data": []}',  # объект с массивом, но не массив
    ]

    for i, content in enumerate(invalid_cases):
        src.write_text(content, encoding="utf-8")
        with pytest.raises(
            ValueError, match="Некорректный формат JSON: ожидается список словарей."
        ):
            json_to_csv(str(src), str(dst))


def test_json_to_csv_invalid_json(tmp_path: Path):
    src = tmp_path / "invalid.json"
    dst = tmp_path / "output.csv"
    src.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_nonexistent_input(tmp_path: Path):
    src = tmp_path / "nonexistent.csv"
    dst = tmp_path / "output.json"

    with pytest.raises(FileNotFoundError):
        csv_to_json(str(src), str(dst))


def test_csv_to_json_invalid_csv(tmp_path: Path):
    src = tmp_path / "invalid.csv"
    dst = tmp_path / "output.json"
    src.write_text("name,age\nAlice", encoding="utf-8")  # Неполная строка

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_csv_to_json_empty_file(tmp_path: Path):
    src = tmp_path / "empty.csv"
    dst = tmp_path / "empty.json"

    with open(src, "w", encoding="utf-8") as f:
        f.write("")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))
```

---

### Скриншоты:

**Задание - A**

![Задание A](../../images/lab07/test_texts.png)

**Задание - B**

![Задание B](../../images/lab07/test_json_csv.png)

**Задание - C**

![Задание C](../../images/lab07/black.png)

**★ Дополнительное задание: покрытие кода**

![Задание D](../../images/lab07/cov.png)

---
