from typing import Any, Generator, Iterator

transactions = [
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


def filter_by_currency(
    transactions_list: list[dict[str, Any]], currency: str
) -> Iterator:
    """Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""

    if transactions_list == [{}]:
        raise ValueError("Некорректные исxодные данные")
    else:
        return (
            x
            for x in transactions_list
            if x["operationAmount"]["currency"]["code"] == currency
        )


def transaction_descriptions(transactions_list: list[dict[str, Any]]) -> Any:
    """Возвращает из списка словарей с транзакциями описание каждой операции по очереди"""

    if transactions_list == [{}]:
        raise ValueError("Некорректные исxодные данные")
    else:
        description = list(
            x["description"] for x in transactions_list if x["description"] != ""
        )
        for item in description:
            yield item


def card_number_generator(start: int, stop: int) -> Generator:
    """Генератор номеров карт"""
    number_zero = "0000000000000000"

    if start > stop:
        print("Начальное значение не может быть больше конечного")

    while (
        start <= stop
        and 0 <= start <= 9999999999999999
        and 0 <= stop <= 9999999999999999
    ):
        card_number_empty = ""
        card_number_str = number_zero[: 16 - len(str(start))] + str(start)
        card_number_total = (
            card_number_empty
            + f"{card_number_str[:4]} {card_number_str[4:8]} {card_number_str[8:12]} {card_number_str[12:]}"
        )
        yield card_number_total
        start += 1


filter_currency = filter_by_currency(transactions, "EUR")
for _ in range(2):
    try:
        print(next(filter_currency))
    except StopIteration:
        print("Нет транзакций с такой валютой")

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))

for card_number in card_number_generator(1, 5):
    print(card_number)
