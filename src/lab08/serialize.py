import json
from typing import List
from models import Student


def students_to_json(students: List[Student], path: str) -> None:
    data = [s.to_dict() for s in students]
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"✅ Студенты сохранены в файл: {path}")


def students_from_json(path: str) -> List[Student]:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            print(f"❌ Ошибка: ожидается список")
            return []

        students = []
        for item in data:
            if not isinstance(item, dict):
                print(f"⚠️ Пропущен элемент: не является словарём — {item}")
                continue
            try:
                student = Student.from_dict(item)
                students.append(student)
            except ValueError as e:
                print(f"⚠️ Не удалось создать студента из данных {item}: {e}")

        print(f"✅ Загружено {len(students)} студентов из файла: {path}")
        return students

    except FileNotFoundError:
        print(f"❌ Файл не найден: {path}")
        return []

    except json.JSONDecodeError as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        return []

    except Exception as e:
        print(f"❌ Непредвиденная ошибка при чтении файла: {e}")
        return []

#Пример 
loaded_students = students_from_json("data/lab08/students_input.json")
for s in loaded_students:
    print (s)
students_to_json(loaded_students, "data/lab08/students_output.json")
