from pathlib import Path
import csv

def read_text(path, encoding = "utf-8"):
    """ Можно выбрать другую кодировку (пример: encoding="cp1251") """
    p = Path(path)
    return p.read_text(encoding=encoding)

def write_csv(rows, path, header=None):
    rows = list(rows)
    if rows:
        cols = len(rows[0])
        for r in rows:
            if len(r) != cols:
                raise ValueError("Строки разной длины")

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        for r in rows:
            writer.writerow(r)
