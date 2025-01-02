import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.external_api import get_amount


def test_get_amount_success(transaction_rub):
    """Тестирует вывод суммы из транзакции в рублях"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 31957.58}
    with patch("requests.get", return_value=mock_response):
        result = float(get_amount(transaction_rub[0]))
        assert result == 31957.58


class TestGetAmount(unittest.TestCase):
    @patch("os.getenv")
    @patch("requests.get")
    def test_get_amount_usd(self, mock_get, mock_getenv):
        """Тестирует конвертор суммы транзакции из USD в рубли"""
        mock_getenv.return_value = "mock_api_key"
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "query": {"from": "USD", "to": "RUB", "amount": 30234.99},
            "info": {"timestamp": 1735397884, "rate": 105.725315},
            "date": "2024-12-28",
            "result": 3196603.841772,
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        transaction_usd = {"operationAmount": {"amount": 30234.99, "currency": {"code": "USD"}}}

        result = get_amount(transaction_usd, load_env=True)
        self.assertEqual(result, 3196603.841772)


class TestGetAmount2(unittest.TestCase):
    @patch("os.getenv")
    @patch("requests.get")
    def test_get_no_transactions_with_amount(self, mock_get, mock_getenv):
        """Проверяет поведение функции при отсутствии суммы в транзакции на стороне сервера"""
        mock_getenv.return_value = "mock_api_key"
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "query": {"from": "USD", "to": "RUB", "amount": 30234.99},
            "info": {"timestamp": 1735397884, "rate": 105.725315},
            "date": "2024-12-28",
            "result": 0.0,
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        transaction_usd = {"operationAmount": {"amount": 30234.99, "currency": {"code": "USD"}}}

        result = get_amount(transaction_usd, load_env=True)
        self.assertEqual(result, 0.0)


class TestGetAmount3(unittest.TestCase):
    @patch("os.getenv")
    @patch("requests.get")
    def test_get_amount_bad_status_code(self, mock_get, mock_getenv):
        """Проверяет поведение функции при неуспешном запросе на сервер"""
        mock_getenv.return_value = "mock_api_key"
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        transaction_usd = {"operationAmount": {"amount": 30234.99, "currency": {"code": "USD"}}}

        with self.assertRaises(ValueError) as context:
            get_amount(transaction_usd, load_env=True)
        self.assertEqual(str(context.exception), "Ошибка API: 401")


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
