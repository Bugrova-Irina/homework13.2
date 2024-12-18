import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "card_account, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ],
)
def test_mask_account_card(card_account: str, expected: str) -> None:
    assert mask_account_card(card_account) == expected


def test_invalid_number_of_card_account(invalid_len_number: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(invalid_len_number)


def test_empty_number_of_card_account(empty_number: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(empty_number)


def test_invalid_letter_number_of_card_account(letter_card_number: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(letter_card_number)


def test_invalid_number_only_one_word(letter_number: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(letter_number)


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-07-25T03:25:10.589654", "25.07.2020"),
    ],
)
def test_get_date(date: str, expected: str) -> None:
    assert get_date(date) == expected


def test_invalid_len_get_date(invalid_len_date: str) -> None:
    with pytest.raises(ValueError):
        get_date(invalid_len_date)


def test_get_date_empty(empty_date: str) -> None:
    with pytest.raises(ValueError):
        get_date(empty_date)


@pytest.mark.parametrize(
    "invalid_date, expected",
    [
        ("20dd-03-11T02:26:18.671407", "Некорректные исходные данные"),
        ("2024-ff-11T02:26:18.671407", "Некорректные исходные данные"),
        ("2024-03-s1T02:26:18.671407", "Некорректные исходные данные"),
    ],
)
def test_get_invalid_date(invalid_date: str, expected: str) -> None:
    with pytest.raises(ValueError):
        get_date(invalid_date)
