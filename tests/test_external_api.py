import os
from unittest.mock import Mock, patch

import pytest
from dotenv import load_dotenv

from src.external_api import get_amount
from tests.conftest import transaction_rub


def test_get_amount_success(transaction_rub):
    """Тестирует вывод суммы из транзакции в рублях"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 31957.58}
    with patch("requests.get", return_value=mock_response):
        result = float(get_amount(transaction_rub[0]))
        assert result == 31957.58


@patch("requests.get")
def test_get_amount_usd(mock_get):
    """Тестирует конвертор суммы транзакции из USD в рубли"""
    load_dotenv()
    apikey = os.getenv("apikey")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 52245.3},
        "info": {"timestamp": 1733938576, "rate": 105.501038},
        "date": "2024-12-11",
        "result": 5511933.380621,
    }

    transaction = {
        "id": 51314762,
        "state": "EXECUTED",
        "date": "2018-08-25T02:58:18.764678",
        "operationAmount": {
            "amount": "52245.30",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 4040551273087672",
        "to": "Visa Platinum 7825450883088021",
    }

    result = get_amount(transaction)
    assert result == 5511933.380621

    currency_transaction = transaction["operationAmount"]["currency"]["code"]
    amount_transaction = transaction["operationAmount"]["amount"]

    expected_url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_transaction}&amount={amount_transaction}"

    assert mock_get.call_count == 1
    mock_get.assert_called_once_with(
        expected_url,
        headers={
            "apikey": apikey,
            "Content-Type": "application/json",
        },
    )


@patch("requests.get")
def test_get_no_transactions_with_amount(mock_get):
    """Проверяет поведение функции при отсутствии суммы в транзакции на стороне сервера"""
    load_dotenv()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    transaction = {
        "id": 51314762,
        "state": "EXECUTED",
        "date": "2018-08-25T02:58:18.764678",
        "operationAmount": {
            "amount": "52245.30",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 4040551273087672",
        "to": "Visa Platinum 7825450883088021",
    }

    assert get_amount(transaction) == 0.0


@patch("requests.get")
def test_get_amount_bad_status_code(mock_get):
    """Проверяет поведение функции при неуспешном запросе на сервер"""
    load_dotenv()
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {}

    transaction = {
        "id": 51314762,
        "state": "EXECUTED",
        "date": "2018-08-25T02:58:18.764678",
        "operationAmount": {
            "amount": "52245.30",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 4040551273087672",
        "to": "Visa Platinum 7825450883088021",
    }

    with pytest.raises(ValueError, match="Ошибка API: 401"):
        get_amount(transaction)

    currency_transaction = transaction["operationAmount"]["currency"]["code"]
    amount_transaction = transaction["operationAmount"]["amount"]
    expected_url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_transaction}&amount={amount_transaction}"

    assert mock_get.call_count == 1
    mock_get.assert_called_once_with(
        expected_url,
        headers={
            "apikey": os.getenv("apikey"),
            "Content-Type": "application/json",
        },
    )


@patch("requests.get")
def test_get_amount_no_apikey(mock_get):
    """Проверяет поведение функции при неуспешном запросе на сервер"""

    os.environ["apikey"] = ""

    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {}

    transaction = {
        "id": 51314762,
        "state": "EXECUTED",
        "date": "2018-08-25T02:58:18.764678",
        "operationAmount": {
            "amount": "52245.30",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 4040551273087672",
        "to": "Visa Platinum 7825450883088021",
    }

    with pytest.raises(ValueError, match="API ключ не найден. Проверьте файл .env"):
        get_amount(transaction)

    assert mock_get.call_count == 0
