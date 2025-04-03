import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from src.vacancy import Vacancy


class AbstractWorkWithVacancy(ABC):
    """Абстрактный класс, содержащий методы, добавляющие вакансии в файл, получающие данные из файла по
    указанным критериям и удаляющие информацию о вакансии"""

    @abstractmethod
    def add_vacancy(self, vacancies):
        """Абстрактный метод предполагающий добавление новых вакансий в JSON файл"""
        pass

    @abstractmethod
    def get_data_from_vacancy(self, requirements):
        """Абстрактный метод, получающий заданную информацию из вакансии"""
        pass

    @abstractmethod
    def delete_vacancy(self, content):
        """Абстрактный метод, удаляющий информацию о вакансии из файла"""
        pass


class JSONSaver(AbstractWorkWithVacancy):
    def __init__(self, path: str = r"../data/vacancies.json"):
        self.__path = Path(path)
        if not self.__path.exists():
            self.save_data([])

    def load_data(self):
        """Приватный метод загрузки данных из JSON-файла."""
        try:
            with open(self.__path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

    def save_data(self, data_):
        """Приватный метод сохранения данных в JSON-файл."""
        try:
            with open(self.__path, "w", encoding="utf-8") as file:
                json.dump(data_, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных в файл: {e}")

    def add_vacancy(self, vacancies):
        """Метод добавления новых вакансий в JSON файл и его сохранение"""
        data_ = self.load_data()
        for vacancy in vacancies:
            vacancy_dict = vacancy.to_dict()
            if vacancy_dict not in data_:
                data_.append(vacancy_dict)
        self.save_data(data_)

    def get_data_from_vacancy(self, query):
        """Возвращает список вакансий, которые соответствуют заданным критериям."""
        data_ = self.load_data()
        result = []
        for i in data_:
            if all(i.get(key) == value for key, value in query.items()):
                result.append(i)
        return result

    def delete_vacancy(self, content):
        """Удаляет вакансии, соответствующие заданным критериям, из JSON-файла."""
        data_ = self.load_data()
        data_ = [
            item
            for item in data_
            if not all(item.get(key) == value for key, value in content.items())
        ]
        self.save_data(data_)
