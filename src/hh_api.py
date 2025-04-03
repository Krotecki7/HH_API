from abc import ABC, abstractmethod
from typing import Dict, List

import requests


class WorkAPI(ABC):
    """Абстрактный класс, как шаблон для работы с платформами. В нем обозначены методы,
    которые должны быть реализованны"""

    @abstractmethod
    def connect(self):
        """Метод для подключения к API сайта"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, page: int = 1):
        """Метод, для получения списка вакансий по поисковому запросу"""
        pass


class HeadHunterAPI(WorkAPI):
    """Kласс, предполагающий получение вакансий с сайта hh.ru, наследуемый от класса WorkAPI."""

    def __init__(self, base_url="https://api.hh.ru/vacancies") -> None:
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def connect(self) -> bool:
        """Метод проверяющий доступность API"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return False

    def get_vacancies(self, search_query: str, per_page: int = 3) -> List[Dict]:
        """Метод получения вакансий с сайта hh.ru. Передаем запрос и количество на страницу"""
        params = {"text": search_query, "per_page": per_page}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return []
