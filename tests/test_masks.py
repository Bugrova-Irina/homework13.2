import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1200567586345678", "1200 56** **** 5678"),
        ("4569000058970124", "4569 00** **** 0124"),
    ],
)
def test_get_mask_card_number(number: str, expected: str) -> None:
    assert get_mask_card_number(number) == expected


def test_get_invalid_card_number(invalid_len_number: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_len_number)
    assert str(exc_info.value) == "Введен некорректный номер карты"


def test_get_invalid_letter_card_number(letter_number: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(letter_number)
    assert str(exc_info.value) == "Введен некорректный номер карты"


def test_get_invalid_empty_card_number(empty_number: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(empty_number)
    assert str(exc_info.value) == "Введен некорректный номер карты"


@pytest.mark.parametrize(
    "number, expected",
    [
        ("12345678912345678913", "**8913"),
        ("00255678912345688888", "**8888"),
        ("11254657860054430699", "**0699"),
    ],
)
def test_get_mask_account(number: str, expected: str) -> None:
    assert get_mask_account(number) == expected


def test_get_invalid_account_number(invalid_len_number: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(invalid_len_number)
    assert str(exc_info.value) == "Введен некорректный номер счета"


def test_get_invalid_letter_account(letter_number: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(letter_number)
    assert str(exc_info.value) == "Введен некорректный номер счета"


def test_get_invalid_empty_account(empty_number: str) -> None:
    with pytest.raises(ValueError):
        get_mask_account(empty_number)
