import json
from unittest.mock import mock_open, patch

import pytest

from src.filter_of_transactions import (get_dict_of_categories,
                                        get_dicts_with_pattern)


def test_get_dicts_with_pattern(transactions_list):
    """
    Тестирует возврат ожидаемого списка словарей,
    у которых в описании есть заданная строка
    """
    mock_data = transactions_list
    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        word = "Перевод со счета на счет"
        result = get_dicts_with_pattern(mock_data, word)
        assert result == [
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {"name": "руб.", "code": "RUB"},
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160",
            },
        ]


def test_get_empty_dicts_with_pattern():
    """
    Тестирует обработку пустого списка словарей и вывод сообщения,
    что нет транзакций
    """
    mock_data = []
    mock_file = json.dumps(mock_data)
    word = "Перевод со счета на счет"

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_dicts_with_pattern(mock_data, word)
        assert result == None


def test_get_bad_dicts_with_pattern():
    """
    Тестирует возбуждение ошибки при обработке некорректных исходных данных
    """
    dicts_list = "kfjgkdfj"
    word = "Перевод со счета на счет"

    with pytest.raises(ValueError, match="Некорректные исходные данные"):
        get_dicts_with_pattern(dicts_list, word)


def test_get_dicts_with_bad_pattern(transactions_list):
    """
    Тестирует получение списка транзакций с несуществующим описанием
    """
    mock_data = transactions_list
    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        word = "Перевод не перевод"
        result = get_dicts_with_pattern(mock_data, word)
        assert result == None


def test_get_dict_of_categories(transactions_list, categories):
    """
    тестирует получение словаря вида
    {'название категории': 'количество операций в каждой категории'}
    """
    mock_data = transactions_list
    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_dict_of_categories(mock_data, categories)
        assert result == {
            "Перевод организации": 2,
            "Перевод со счета на счет": 2,
            "Перевод с карты на карту": 1,
        }


def test_get_empty_dict_of_categories(categories):
    """
    тестирует получение словаря вида
    {'название категории': 'количество операций в каждой категории'}
    из пустого списка словарей
    """

    mock_data = []
    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_dict_of_categories(mock_data, categories)
        assert result == "Нет категорий для подсчета"


def test_get_bad_dicts_of_categories(categories):
    """
    Тестирует возбуждение ошибки при обработке некорректных исходных данных
    """
    dicts_list = "kfjgkdfj"

    with pytest.raises(ValueError, match="Некорректные исходные данные"):
        get_dict_of_categories(dicts_list, categories)


def test_get_dicts_with_bad_categories(transactions_list):
    """
    Тестирует подсчет категорий, которых нет в описании транзакций
    """
    mock_data = transactions_list
    mock_file = json.dumps(mock_data)
    categories = ["fdfd"]

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_dict_of_categories(mock_data, categories)
        assert result == "Нет категорий для подсчета"
