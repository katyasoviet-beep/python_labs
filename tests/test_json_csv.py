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
