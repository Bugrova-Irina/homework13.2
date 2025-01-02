import json
from unittest.mock import mock_open, patch

import pytest

from src.main import (get_user_filter_by_currency, get_user_filter_transactions_by_word, get_user_path,
                      get_user_sort_by_date, get_user_status_of_transactions, main)
from tests.conftest import transactions_list


@pytest.fixture
def mock_input_choice():
    with patch("builtins.input", side_effect=lambda prompt: "1"):
        yield


def test_get_user_path(mock_input_choice):
    """
    тестирует получение пути к файлу на основе выбора пользователя
    """
    result = get_user_path()
    assert result == "../homework13.2/data/operations.json"


@pytest.fixture
def mock_bad_input_choice():
    with patch("builtins.input", side_effect=["4", "2"]):
        yield


def test_get_bad_user_path(mock_bad_input_choice):
    """
    тестирует возврат к началу выбора, если выбран неверный пункт меню
    """
    result = get_user_path()
    assert result == "../homework13.2/data/transactions.csv"


@pytest.fixture
def mock_input_status():
    with patch("builtins.input", side_effect=lambda prompt: "EXECUTED"):
        yield


def test_get_user_status_of_transactions(mock_input_status):
    """
    тестирует получение статуса на основе выбора пользователя
    """
    result = get_user_status_of_transactions()
    assert result == "EXECUTED"


@pytest.fixture
def mock_bad_input_status():
    with patch("builtins.input", side_effect=["jdfdgk", "EXECUTED"]):
        yield


def test_get_bad_user_status(mock_bad_input_status):
    """
    тестирует возврат к началу выбора, если выбран неверный статус
    """
    result = get_user_status_of_transactions()
    assert result == "EXECUTED"


@pytest.fixture
def mock_input_sort_by_date():
    with patch("builtins.input", side_effect=["да", "по возрастанию"]):
        yield


def test_get_user_sort_by_date(mock_input_sort_by_date):
    """
    тестирует правильный ввод ответов пользователя на вопрос
    о сортировке по дате с первой попытки
    """
    result = get_user_sort_by_date()
    assert result == False


@pytest.fixture
def mock_bad_first_input_sort_by_date():
    with patch("builtins.input", side_effect=["1", "нет"]):
        yield


def test_get_first_bad_user_sort_by_date(mock_bad_first_input_sort_by_date):
    """
    тестирует обработку неправильного ответа пользователя
    и отказ от сортировки по дате
    """
    result = get_user_sort_by_date()
    assert result == None


@pytest.fixture
def mock_bad_second_input_sort_by_date():
    with patch("builtins.input", side_effect=["да", "н", "да", "по убыванию"]):
        yield


def test_get_second_bad_user_sort_by_date(mock_bad_second_input_sort_by_date):
    """
    тестирует обработку неправильного ответа пользователя на вопрос 'как сортировать?'
    """
    result = get_user_sort_by_date()
    assert result == True


@pytest.fixture
def mock_input_sort_by_currency():
    with patch("builtins.input", side_effect=lambda prompt: "да"):
        yield


def test_get_user_sort_by_currency(mock_input_sort_by_currency):
    """
    тестирует получение верного ответа пользователя на вопрос,
    по какой валюте сортировать
    """
    result = get_user_filter_by_currency()
    assert result == "RUB"


@pytest.fixture
def mock_bad_input_sort_by_currency():
    with patch("builtins.input", side_effect=["hfg", "нет"]):
        yield


def test_get_bad_user_sort_by_currency(mock_bad_input_sort_by_currency):
    """
    тестирует обработку неправильного ответа пользователя на вопрос,
    по какой валюте сортировать
    """
    result = get_user_filter_by_currency()
    assert result == "USD"


@pytest.fixture
def mock_input_user_filter_transactions_by_word():
    with patch("builtins.input", side_effect=lambda prompt: "да"):
        yield


def test_get_user_filter_transactions_by_word(
    mock_input_user_filter_transactions_by_word,
):
    """
    тестирует получение верного ответа пользователя на вопрос,
    нужно ли сортировать по слову в описании транзакции
    """
    result = get_user_filter_transactions_by_word()
    assert result == "да"


@pytest.fixture
def mock_bad_input_user_filter_transactions_by_word():
    with patch("builtins.input", side_effect=["ff", "да", "вклада"]):
        yield


def test_get_bad_user_filter_transactions_by_word(
    mock_bad_input_user_filter_transactions_by_word,
):
    """
    тестирует обработку неправильного ответа пользователя на вопрос,
    нужно ли сортировать по слову в описании транзакции
    """
    result = get_user_filter_transactions_by_word()
    assert result == "вклада"


@pytest.fixture
def mock_input_user_no_filter_transactions_by_word():
    with patch("builtins.input", side_effect=lambda prompt: "нет"):
        yield


def test_get_user_no_filter_transactions_by_word(
    mock_input_user_no_filter_transactions_by_word,
):
    """
    тестирует получение ответа "нет" от пользователя на вопрос,
    нужно ли сортировать по слову в описании транзакции
    """
    result = get_user_filter_transactions_by_word()
    assert result == None


@pytest.fixture
def mock_open_json_file(transactions_list):  # мокируем открытие файла
    m = mock_open(read_data=json.dumps(transactions_list))
    with patch("builtins.open", m):
        yield


@pytest.fixture
def mock_input_main_from_json(mock_open_json_file):  # мокируем ответы пользователя
    inputs = [
        "1",  # Выберите необходимый пункт меню
        "EXECUTED",  # Введите статус
        "нет",  # Отсортировать операции по дате?
        "нет",  # Выводить только рублевые транзакции?
        "да",  # Отфильтровать список транзакций по определенному слову в описании?
        "на карту",  # Введите слово или строку для фильтрации
    ]
    with patch("builtins.input", side_effect=inputs):
        yield


def test_main_from_json(mock_input_main_from_json):
    """
    Тестируем вывод транзакции по заданным пользователем параметрам из json-файла
    """
    # expected_output = """
    #             Распечатываю итоговый список транзакций...
    #             Всего банковских операций в выборке: 1
    #
    #             19.08.2018 Перевод с карты на карту
    #             Visa Classic 6831 98** **** 7658 Visa Platinum 8990 92** **** 5229
    #             56883.54: USD.
    #         """.strip()

    assert main() == None


@pytest.fixture
# мокируем открытие файла
def mock_open_csv_or_xlsx_file(transactions_list, csv_or_xlsx_transactions_list):
    m = mock_open(read_data=json.dumps(csv_or_xlsx_transactions_list))
    with patch("builtins.open", m):
        yield


@pytest.fixture
# мокируем ответы пользователя
def mock_input_main_from_csv_or_xlsx(mock_open_csv_or_xlsx_file):
    inputs = [
        "1",  # Выберите необходимый пункт меню
        "EXECUTED",  # Введите статус
        "нет",  # Отсортировать операции по дате?
        "нет",  # Выводить только рублевые транзакции?
        "да",  # Отфильтровать список транзакций по определенному слову в описании?
        "на карту",  # Введите слово или строку для фильтрации
    ]
    with patch("builtins.input", side_effect=inputs):
        yield


def test_main_from_csv_or_xlsx(mock_input_main_from_csv_or_xlsx):
    """
    Тестируем вывод транзакции по заданным пользователем
    параметрам из csv или xlsx-файла
    """
    # expected_output = """
    #             Распечатываю итоговый список транзакций...
    #             Всего банковских операций в выборке: 1
    #
    #             19.08.2018 Перевод с карты на карту
    #             Visa Classic 6831 98** **** 7658 Visa Platinum 8990 92** **** 5229
    #             56883.54: USD.
    #         """.strip()

    assert main() == None


@pytest.fixture
def mock_open_json_file_for_main(transactions_list):  # мокируем открытие файла
    m = mock_open(read_data=json.dumps(transactions_list))
    with patch("builtins.open", m):
        yield


@pytest.fixture
# мокируем ответы пользователя
def mock_input_main_from_json_with_missing_word(mock_open_json_file_for_main):
    inputs = [
        "1",  # Выберите необходимый пункт меню
        "EXECUTED",  # Введите статус
        "нет",  # Отсортировать операции по дате?
        "нет",  # Выводить только рублевые транзакции?
        "да",  # Отфильтровать список транзакций по определенному слову в описании?
        "ромашка",  # Введите слово или строку для фильтрации
    ]
    with patch("builtins.input", side_effect=inputs):
        yield


def test_main_from_json_with_missing_word(mock_input_main_from_json_with_missing_word):
    """
    Тестируем вывод транзакции по заданным пользователем параметрам
    по отсутствующему в описании транзакции слову
    """

    assert main() == "Произошла ошибка object of type 'NoneType' has no len()"


@pytest.fixture
def mock_open_json_file_for_main_without_word(
    transaction_rub,
):  # мокируем открытие файла
    m = mock_open(read_data=json.dumps(transaction_rub))
    with patch("builtins.open", m):
        yield


@pytest.fixture
# мокируем ответы пользователя
def mock_input_main_from_json_without_word(mock_open_json_file_for_main_without_word):
    inputs = [
        "1",  # Выберите необходимый пункт меню
        "EXECUTED",  # Введите статус
        "нет",  # Отсортировать операции по дате?
        "нет",  # Выводить только рублевые транзакции?
        "нет",  # Отфильтровать список транзакций по определенному слову в описании?
    ]
    with patch("builtins.input", side_effect=inputs):
        yield


def test_main_from_json_without_word(mock_input_main_from_json_without_word):
    """
    Тестируем вывод транзакции по заданным пользователем параметрам
    (транзакции в USD) без фильтра по слову в описании транзакции
    """
    # excepted_result = Не найдено ни одной транзакции, подходящей под ваши условия фильтрации
    assert main() == None


@pytest.fixture
def mock_open_json_file_for_main_ruble_without_word(
    transaction_rub,
):  # мокируем открытие файла
    m = mock_open(read_data=json.dumps(transaction_rub))
    with patch("builtins.open", m):
        yield


@pytest.fixture
# мокируем ответы пользователя
def mock_input_main_from_json_ruble_without_word(
    mock_open_json_file_for_main_ruble_without_word,
):
    inputs = [
        "1",  # Выберите необходимый пункт меню
        "EXECUTED",  # Введите статус
        "нет",  # Отсортировать операции по дате?
        "да",  # Выводить только рублевые транзакции?
        "нет",  # Отфильтровать список транзакций по определенному слову в описании?
    ]
    with patch("builtins.input", side_effect=inputs):
        yield


def test_main_from_json_ruble_without_word(
    mock_input_main_from_json_ruble_without_word,
):
    """
    Тестируем вывод транзакции по заданным пользователем параметрам
    (транзакции в рублях) без фильтра по слову в описании транзакции
    """
    # excepted_result = """
    # Распечатываю итоговый список транзакций...
    # Всего банковских операций в выборке: 1
    #
    #                         26.08.2019 Перевод организации
    #                         Maestro 1596 83** **** 5199 Счет **9589
    #                         31957.58: руб.
    # """
    assert main() == None
