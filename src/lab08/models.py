# Импортируем необходимые модули
from dataclasses import dataclass  # Чтобы использовать @dataclass
from datetime import datetime, date  # Для работы с датами


@dataclass
class Student:
    # Поля класса с указанием типов
    # Это значит: fio — строка, birthdate — строка, group — строка, gpa — число (дробное)
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        # Этот метод вызывается автоматически ПОСЛЕ __init__
        # Здесь мы проверяем, что данные корректны

        # Проверяем формат даты: должна быть в виде "2000/12/31"
        try:
            # Пытаемся преобразовать строку birthdate в дату по формату ГГГГ/ММ/ДД
            datetime.strptime(self.birthdate, "%Y/%m/%d")
            # Если всё прошло без ошибок — формат правильный
        except ValueError:
            # Если формат неправильный, выбрасываем исключение
            # (лучше так, чем просто print — программа не продолжит работу с битыми данными)
            raise ValueError(f"Неверный формат даты: '{self.birthdate}'. Ожидается ГГГГ/ММ/ДД")

        # Проверяем, что средний балл (gpa) в диапазоне от 0 до 5
        if not (0 <= self.gpa <= 5):
            # Если gpa < 0 или gpa > 5 — ошибка
            raise ValueError("gpa должен быть от 0 до 5 включительно")

    def age(self) -> int:
        # Метод для вычисления возраста студента в годах

        # Сначала преобразуем строку birthdate в реальную дату
        birth = datetime.strptime(self.birthdate, "%Y/%m/%d").date()
        # Например: "2000/05/20" → объект даты 20 мая 2000 года

        # Получаем текущую дату (сегодня)
        today = date.today()

        # Считаем разницу в годах
        # Но: если день рождения ещё не наступил в этом году — вычитаем 1
        # Например: сегодня 10 марта 2024, а родился 15 мая 2000 — ещё нет 24 лет, только 23
        age = today.year - birth.year  # сначала просто разница лет
        # Проверяем: если (месяц, день) сегодня меньше, чем у дня рождения — ещё не было ДР
        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1  # уменьшаем на 1, если день рождения ещё впереди

        return age  # возвращаем возраст как целое число

    def to_dict(self) -> dict:
        # Метод превращает объект Student в словарь (полезно для сохранения в JSON)
        return {
            "fio": self.fio,        # ФИО — как есть
            "birthdate": self.birthdate,  # Дата рождения — как есть (строка)
            "group": self.group,    # Группа
            "gpa": self.gpa         # Средний балл
        }

    @classmethod
    def from_dict(cls, d: dict):
        # Метод создаёт объект Student из словаря
        # cls — это сам класс Student (аналогично вызову Student(...))
        return cls(
            fio=d["fio"],           # берём fio из словаря
            birthdate=d["birthdate"],
            group=d["group"],
            gpa=d["gpa"]
        )

    def __str__(self):
        # Метод возвращает строковое представление объекта
        # Это то, что будет выводиться, если написать print(student)
        return f"{self.fio}, {self.birthdate}, {self.group}, {self.gpa}"
        
# Пример
'''
s = Student("Иванов Иван Иванович", "2005/05/15", "SE-01", 4.5)
print(s)                   
print(s.age())              
data = s.to_dict()
print(data)          
s2 = Student.from_dict(data) 
print(s2)
'''
