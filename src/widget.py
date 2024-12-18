from src import masks


def mask_account_card(number_of_account_card: str) -> str:
    """Функция маскировки номера карты или счета"""

    # получаем номер из номера карты или счета
    new_number = ""

    if number_of_account_card == "":
        raise ValueError("Введите номер карты")

    for symbol in number_of_account_card:
        if symbol.isdigit():
            new_number += symbol
    if new_number == "":
        raise ValueError("Введите номер карты")

    # заменяем номер карты или счета на маску
    list_items_of_card_number = number_of_account_card.split()
    for word in list_items_of_card_number:
        if word == new_number:
            if len(new_number) == 16:
                mask_new_numer = masks.get_mask_card_number(new_number)
            else:
                mask_new_numer = masks.get_mask_account(new_number)
            list_items_of_card_number[-1] = mask_new_numer
    mask_number = " ".join(list_items_of_card_number)
    return mask_number


def get_date(date: str) -> str:
    """Функция форматирования даты"""
    if date == "":
        raise ValueError("Введите дату")
    elif len(date) != 26:
        raise ValueError("Некорректные исходные данные")
    elif not date[:4].isdigit() or not date[5:7].isdigit() or not date[8:10].isdigit():
        raise ValueError("Некорректные исходные данные")
    else:
        date_list = [date[8:10], date[5:7], date[:4]]
        formated_date = ".".join(date_list)
        return formated_date
