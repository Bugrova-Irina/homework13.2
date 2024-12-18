from typing import Any

import pytest


@pytest.fixture
def invalid_len_number() -> str:
    return "1254646"


@pytest.fixture
def letter_number() -> str:
    return "sdsfdsgdf"


@pytest.fixture
def empty_number() -> str:
    return ""


@pytest.fixture
def invalid_len_date() -> str:
    return "2024-03-11T02:26:18.67140"


@pytest.fixture
def empty_date() -> str:
    return ""


@pytest.fixture
def letter_card_number() -> str:
    return "master sdsfdsgdf"


@pytest.fixture
def list_of_dicts_with_invalid_status() -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "fgd", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "dff", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "sgdh", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_of_dicts_with_invalid_dates() -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "dd19-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "sss-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "qww-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2015-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def transactions_list() -> list[dict[str, Any]]:
    return [
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
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def transactions():
    return [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 150, "currency": "EUR"},
        {"id": 3, "amount": 200, "currency": "RUB"},
    ]


@pytest.fixture
def transaction_rub():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        }
    ]
