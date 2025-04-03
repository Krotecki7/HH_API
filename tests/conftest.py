import os

import pytest

from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy


@pytest.fixture()
def head_hunter_example():
    """Фикстура экземпляр класса HHJobPlatform"""
    return HeadHunterAPI(base_url="https://api.hh.ru/vacancies")


@pytest.fixture
def vacancy_python_developer():
    """Фикстура класса Vacancy пайтон разработчик"""
    return Vacancy(
        name="Python_developer",
        url="https://hh.ru/applicant/vacancy_response?vacancyId=117286365",
        salary_from=100000,
        salary_to=120000,
        description="Разработка и поддержка, back end части веб-приложений.",
    )


@pytest.fixture
def vacancy_system_administrator():
    """Фикстура класса Vacancy системный аналитик"""
    return Vacancy(
        name="Системный администратор",
        url="https://hh.ru/applicant/vacancy_response?vacancyId=112451122",
        salary_from=50000,
        salary_to=90000,
    )


@pytest.fixture
def mock_hh_api():
    """Создаем mock-объект для HHJobPlatform."""
    platform = HeadHunterAPI(base_url="https://api.hh.ru/vacancies")
    return platform


@pytest.fixture()
def vacancy_without_name():
    """Фикстура, возвращающая данные для создания вакансии без имени."""
    return {
        "name": "",
        "url": "https://hh.com/job1",
        "salary_from": 60000,
        "salary_to": 120000,
    }


@pytest.fixture()
def vacancy_without_url():
    """Фикстура, возвращающая данные для создания вакансии без адреса url."""
    return {"name": "Сантехник", "url": "", "salary_from": 60000, "salary_to": 120000}


@pytest.fixture()
def vacancy_with_negative_salary():
    """Фикстура, возвращающая данные для создания вакансии, где зарплата - отрицательное число."""
    return {
        "name": "Садовник",
        "url": "https://hh.com/job2",
        "salary_from": -60000,
        "salary_to": 120000,
    }


@pytest.fixture()
def vacancy_with_salary_to_less_salary_from():
    """Фикстура, возвращающая данные для создания вакансии, где зарплата - отрицательное число."""
    return {
        "name": "Бухгалтер",
        "url": "https://hh.com/job3",
        "salary_from": 120000,
        "salary_to": 100000,
    }


@pytest.fixture()
def platform_data():
    """Фикстура с данными, которые возвращает платформа."""
    return [
        {
            "name": "Программист",
            "apply_alternate_url": "https://example.com/job1",
            "salary": {"from": 80000, "to": 150000},
            "department": {"name": "Отдел разработки"},
        },
        {
            "name": "Тестировщик",
            "apply_alternate_url": "https://example.com/job2",
            "salary": {"from": 60000, "to": 100000},
            "department": {"name": "Отдел тестирования"},
        },
    ]


@pytest.fixture
def temp_json_file(tmp_path):
    """Фикстура для создания временного JSON-файла в тестах."""
    file = tmp_path / "test_vacancies.json"
    yield file
    if file.exists():
        os.remove(file)


@pytest.fixture
def hh_platform():
    """Фикстура, создающая экземпляр HHJobPlatform с базовым URL."""
    return HeadHunterAPI()
