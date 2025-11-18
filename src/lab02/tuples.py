from typing import Tuple

StudentRecord = Tuple[str, str, float]


def format_record(rec: StudentRecord) -> str:
    fio, group, gpa = rec
    if not fio.strip() or not group.strip():
        raise ValueError("ФИО и группа не могут быть пустыми.")
    if not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом (int или float).")
    fio_parts = [part.strip() for part in fio.split()]
    initials = "".join(part[0].upper() + "." for part in fio_parts[1:])
    formatted_gpa = f"{gpa:.2f}"
    formatted_record = (
        f"{fio_parts[0]} {initials}, гр. {group.strip()}, GPA {formatted_gpa}"
    )
    return formatted_record


# Тест-кейсы
print(format_record(("Иванов Иван Иванович", "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))


# Свои примеры
print(format_record(("Советская Екатерина Алексеевна", "BIVT-25", 4.3)))
print(format_record(("Романов Николай", "IKBO-13", 5.0)))
print(format_record(("Романов Николай Александрович", "IKBO-13", 5.0)))
print(format_record(("       советская   екатерина     алексеевна   ", "BIVT-25", 4.3)))


# Примеры некорректных записей
try:
    print(format_record(("", "BIVT-25", 4.6)))
except ValueError as e:
    print(e)
try:
    print(format_record(("Иванов Иван", "", 4.6)))
except ValueError as e:
    print(e)
try:
    print(format_record(("Иванов Иван", "BIVT-25", "четыре")))
except TypeError as e:
    print(e)
