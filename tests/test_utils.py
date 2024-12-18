import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import generate_transaction, get_transactions


def test_get_transactions():
    """Тестирует возврат списка транзакций из json-файла"""
    mock_data = [
        {
            "id": 558167602,
            "state": "EXECUTED",
            "date": "2019-04-12T17:27:27.896421",
            "operationAmount": {
                "amount": "43861.89",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 73654108430135874305",
            "to": "Счет 89685546118890842412",
        }
    ]

    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_transactions("mock_path.json")
        assert result == mock_data


def test_get_empty_transactions():
    """Тестирует возврат пустого списка транзакций из пустого json-файла"""
    mock_data = []
    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_transactions("mock_path.json")
        assert result == mock_data


def test_get_bad_transactions():
    """Тестирует возврат списка транзакций из некорректного json-файла"""
    mock_data = "fdgfdg"

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_transactions("mock_path.json")
        assert result == []


@patch("random.choice")
def test_generate_transactions(mock_choice, transactions):
    """Тестирует генератор транзакций"""
    mock_choice.side_effect = transactions

    transaction_generator = generate_transaction(transactions)

    transaction1 = next(transaction_generator)
    transaction2 = next(transaction_generator)

    assert transaction1 in transactions
    assert transaction2 in transactions

    assert mock_choice.call_count == 2


def test_generate_no_transactions():
    """тестирует генератор транзакций при их отсутствии"""
    with pytest.raises(ValueError) as exc_info:
        next(generate_transaction([]))
    assert str(exc_info.value) == "Список транзакций пуст."


# @patch("random.choice")
# def test_generate_bad_transactions(mock_choice, transactions):
#     """Тестирует генератор транзакций с некорректными входными данными"""
#     mock_choice.side_effect = ValueError("Некорректные исходные данные {e}")
#
#     with pytest.raises(ValueError, match="Некорректные исходные данные {e}"):
#         transaction_generator = generate_transaction([546546])
#         next(transaction_generator)
#         yield "Некорректные исходные данные {e}"
