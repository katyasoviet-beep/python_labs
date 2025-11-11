from pathlib import Path
import csv
from openpyxl import Workbook

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    csv_file = Path(csv_path)
    with csv_file.open('r', encoding='utf-8') as c: # открываем файл с формате чтения, кодировка utf-8
        reader = csv.reader(c)
        rows = list(reader)
        print(rows)
    if not rows or not rows[0]:
        raise ValueError("Пустой CSV или неправильный формат.")
    wb = Workbook()
    ws = wb.active
    ws.title = 'Sheet1'
    for row in rows:
        ws.append(row)
    for column_cells in ws.columns:
        max_length = 0
        for cell in column_cells:
            value_len = len(str(cell.value)) if cell.value else 0
            max_length = max(value_len, max_length)
        adjusted_width = max(max_length + 2, 8)  # Добавляем пару символов и устанавливаем минимум 8 символов
        ws.column_dimensions[column_cells[0].column_letter].width = adjusted_width
    wb.save('data/out/xlsx_path.xlsx')

# Тест
csv_to_xlsx('data/samples/cities.csv', xlsx_path='data/out/xlsx_path.xlsx')