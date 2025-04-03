from typing import Dict, List


class Vacancy:

    __slots__ = ("name", "url", "salary_from", "salary_to", "description")

    def __init__(self, name, url, salary_from=None, salary_to=None, description=None):
        self.name = name
        self.url = url
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.description = description or "Описание не указано"

        self.__validate()

    def __validate(self) -> None:
        """Метод для валидации данных вакансии"""
        if not self.name or not self.url:
            raise ValueError("Должны быть указаны имя и url адрес")
        if self.salary_from < 0 or self.salary_to < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        if self.salary_from is None and self.salary_to is None:
            if self.salary_from > self.salary_to:
                raise ValueError(
                    "Минимальная зарплата не может быть больше максимальной."
                )

    def __str__(self) -> str:
        """Метод строкового отображения вакансии"""
        return f"Вакансия: {self.name}, зарплата: от {self.salary_from} до {self.salary_to}, URL-адрес: {self.url}"

    def __lt__(self, other: "Vacancy") -> bool:
        """Метод, сравнивающий вакансии по минимальной ЗП"""
        return (self.salary_from + self.salary_to) / 2 < (
            other.salary_from + other.salary_to
        ) / 2

    def __gt__(self, other: "Vacancy") -> bool:
        """Метод, сравнивающий вакансии по максимальной ЗП"""
        return (self.salary_from + self.salary_to) / 2 > (
            other.salary_from + other.salary_to
        ) / 2

    @staticmethod
    def cast_to_object_list(vacancies: List[Dict]) -> List:
        """Преобразование набора данных из JSON в список объектов"""
        result_vacancy = []
        for info in vacancies:
            name = info.get("name", "Название не указано")
            url = info.get("apply_alternate_url")
            salary_from = (
                info.get("salary", {}).get("from", 0) if info.get("salary") else 0
            )
            # Если есть salary, Обращаемся к вакансии по ключу salary, внутри обращаемся по ключу "from"
            salary_to = info.get("salary", {}).get("to", 0) if info.get("salary") else 0

            department = info.get("department")
            description = (
                department.get("name", "Описание не указано")
                if department
                else "Описание не указано"
            )

            vacancy = Vacancy(
                name=name,
                url=url,
                salary_from=salary_from,
                salary_to=salary_to,
                description=description,
            )

            result_vacancy.append(vacancy)

        return result_vacancy

    def to_dict(self) -> Dict:
        """Метод, преобразующий объект класса в словарь"""
        return {
            "name": self.name,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "description": self.description,
        }
