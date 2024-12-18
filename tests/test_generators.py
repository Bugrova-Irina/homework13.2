from typing import Any

import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


def test_filter_by_currency(transactions_list: list[dict[str, Any]]) -> None:
    generator = filter_by_currency(transactions_list, "USD")
    assert next(generator) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }


def test_empty_transactions() -> None:
    with pytest.raises(ValueError) as exc_info:
        filter_by_currency([{}], "USD")
    assert str(exc_info.value) == "Некорректные исxодные данные"


@pytest.mark.parametrize(
    "transactions_list, currency, expected",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {
                        "amount": "9824.07",
                        "currency": {"name": "USD", "code": "USD"},
                    },
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
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
            ],
            "EUR",
            "Нет транзакций с такой валютой",
        ),
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {
                        "amount": "9824.07",
                        "currency": {"name": "USD", "code": "USD"},
                    },
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
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
            ],
            "GBP",
            "Нет транзакций с такой валютой",
        ),
    ],
)
def test_filter_by_other_currency(
    transactions_list: list[dict[str, Any]], currency: str, expected: str
) -> None:
    generator = filter_by_currency(transactions_list, currency)
    try:
        print(next(generator))
    except StopIteration:
        print("Нет транзакций с такой валютой")


@pytest.mark.parametrize(
    "transactions_list, expected",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {
                        "amount": "9824.07",
                        "currency": {"name": "USD", "code": "USD"},
                    },
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                }
            ],
            "Перевод организации",
        ),
        (
            [
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
                }
            ],
            "Перевод со счета на счет",
        ),
    ],
)
def test_transaction_description(
    transactions_list: list[dict[str, Any]], expected: str
) -> None:
    generator = transaction_descriptions(transactions_list)
    assert next(generator) == expected


def test_empty_transaction_descriptions() -> None:
    with pytest.raises(ValueError):
        generator = transaction_descriptions([{}])
        assert next(generator) == "Некорректные исxодные данные"


def test_transaction_with_5_description(
    transactions_list: list[dict[str, Any]]
) -> None:
    generator = transaction_descriptions(transactions_list)
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод с карты на карту"
    assert next(generator) == "Перевод организации"


def test_card_number_generator() -> None:
    generator = card_number_generator(52345, 52349)
    assert next(generator) == "0000 0000 0005 2345"
    assert next(generator) == "0000 0000 0005 2346"
    assert next(generator) == "0000 0000 0005 2347"
    assert next(generator) == "0000 0000 0005 2348"
    assert next(generator) == "0000 0000 0005 2349"


def test_invalid_start_stop() -> None:
    generator = card_number_generator(5, 4)
    try:
        print(next(generator))
    except StopIteration:
        print("Начальное значение не может быть больше конечного")


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (-2, -1, None),
        (5, 4, None),
        (19999999999999900, 19999999999999999, None),
        ("dsds", "1 2", None),
    ],
)
def test_negative_start_stop(start: int, stop: int, expected: None) -> None:
    generator = card_number_generator(start, stop)
    assert print(generator) == expected
