from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        try:
            datetime.strptime(self.birthdate, "%Y/%m/%d")
        except ValueError:
            raise ValueError(f"Неверный формат даты: '{self.birthdate}'. Ожидается ГГГГ/ММ/ДД")

        if not (0 <= self.gpa <= 5):
            raise ValueError("gpa должен быть от 0 до 5 включительно")

    def age(self) -> int:
        birth = datetime.strptime(self.birthdate, "%Y/%m/%d").date()
        today = date.today()

        age = today.year - birth.year 
        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1  

        return age  

    def to_dict(self) -> dict:
        return {
            "fio": self.fio,      
            "birthdate": self.birthdate, 
            "group": self.group,    
            "gpa": self.gpa         
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            fio=d["fio"],     
            birthdate=d["birthdate"],
            group=d["group"],
            gpa=d["gpa"]
        )

    def __str__(self):
        return f"{self.fio}, {self.birthdate}, {self.group}, {self.gpa}"
        
# Пример

s = Student("Иванов Иван Иванович", "2005/05/15", "SE-01", 4.5)
print(s)                   
print(s.age())              
data = s.to_dict()
print(data)          
s2 = Student.from_dict(data) 
print(s2)

