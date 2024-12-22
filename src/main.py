import json
from typing import Any

from filter_of_transactions import get_dicts_with_pattern
from generators import filter_by_currency
from get_from_csv_xlsx import get_transactions_csv, get_transactions_xlsx
from processing import filter_by_state, sort_by_date
from widget import get_date, mask_account_card


def get_user_path() -> str:
    """Определяет, из какого файла считывать транзакции"""

    user_choice = input(
        """
        Привет! Добро пожаловать в программу работы
        с банковскими транзакциями.
        Выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла\n
        """
    )
    user_file_path = ""

    if user_choice == "1":
        user_file_path = "../homework13.2/data/operations.json"
        print("Для обработки выбран JSON-файл")
    elif user_choice == "2":
        user_file_path = "../homework13.2/data/transactions.csv"
        print("Для обработки выбран CSV-файл")
    elif user_choice == "3":
        user_file_path = "../homework13.2/data/transactions_excel.xlsx"
        print("Для обработки выбран XLSX-файл")
    else:
        print("Введен неверный номер пункта меню")
        get_user_path()  # Повторяем вопрос пользователю

    return user_file_path


def get_user_status_of_transactions() -> str:
    """Определяет статус транзакций, которые нужны пользователю."""

    user_input_status = input(
        """
        Введите статус, по которому необходимо выполнить фильтрацию.
        Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
        """
    ).upper()

    if user_input_status == "EXECUTED":
        print('\nОперации отфильтрованы по статусу "EXECUTED"')
        return user_input_status
    elif user_input_status == "CANCELED":
        print('\nОперации отфильтрованы по статусу "CANCELED"')
        return user_input_status
    elif user_input_status == "PENDING":
        print('\nОперации отфильтрованы по статусу "PENDING"')
        return user_input_status
    else:
        print(f"Статус операции {user_input_status} недоступен")
        return get_user_status_of_transactions()  # Повторяем вопрос пользователю


def get_user_sort_by_date() -> Any:
    """Уточняет у пользователя, нужна ли сортировка транзакций по дате"""

    user_input_sort_by_date = input(
        "\nОтсортировать операции по дате? (да/нет)\n"
    ).lower()

    if user_input_sort_by_date == "да":
        user_input_sort_by_date_reverse = input(
            "\nОтсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию)\n"
        ).lower()
        if user_input_sort_by_date_reverse == "по убыванию":
            return True
        elif user_input_sort_by_date_reverse == "по возрастанию":
            return False
        else:
            print("Некорректный ввод. Попробуйте еще раз.")
            return get_user_sort_by_date()  # Повторяем вопрос пользователю
    elif user_input_sort_by_date == "нет":
        return None
    else:
        print("Некорректный ввод. Попробуйте еще раз.")
        return get_user_sort_by_date()  # Повторяем вопрос пользователю


def get_user_filter_by_currency() -> str:
    """Уточняет у пользователя, в какой валюте выводить транзакции"""

    user_input_currency = input("\nВыводить только рублевые транзакции? (да/нет)\n")
    if user_input_currency == "да":
        return "RUB"
    elif user_input_currency == "нет":
        return "USD"
    else:
        return get_user_filter_by_currency()  # Повторяем вопрос пользователю


def get_user_filter_transactions_by_word() -> Any:
    """Уточняет у пользователя, по какому слову в описании фильтровать транзакции"""

    user_input_word_for_filter_transactions = input(
        "\nОтфильтровать список транзакций по определенному слову в описании? (да/нет)\n"
    ).lower()
    if user_input_word_for_filter_transactions == "да":
        user_filter_word = input("\nВведите слово или строку для фильтрации:\n")
        return user_filter_word
    elif user_input_word_for_filter_transactions == "нет":
        return None
    else:
        return get_user_filter_transactions_by_word()  # Повторяем вопрос пользователю


def main() -> Any:
    """Выводит транзакции по ранее заданным параметрам"""
    # Определяем, из какого файла брать транзакции
    user_path = get_user_path()
    if user_path == "../homework13.2/data/operations.json":
        with open(user_path, encoding="utf-8") as file:
            list_dicts = json.load(file)

    elif user_path == "../homework13.2/data/transactions.csv":
        list_dicts = get_transactions_csv(user_path)

    else:
        list_dicts = get_transactions_xlsx(user_path)

    # Определяем, по какому статусу фильтровать транзакции
    transaction_status = get_user_status_of_transactions()
    list_dicts_filtered_by_state = filter_by_state(list_dicts, transaction_status)

    # Сортируем транзакции по дате, если нужно
    user_sort_by_date = get_user_sort_by_date()
    list_dicts_sort_by_date = list_dicts_filtered_by_state
    if isinstance(user_sort_by_date, bool):
        list_dicts_sort_by_date = sort_by_date(
            list_dicts_filtered_by_state, user_sort_by_date
        )

    # Фильтруем транзакции по валюте
    user_filter_by_currency = get_user_filter_by_currency()
    list_dicts_filtered_by_currency = filter_by_currency(
        list_dicts_sort_by_date, user_filter_by_currency
    )
    filtered_transactions = list(list_dicts_filtered_by_currency)

    # Фильтруем транзакции по слову в поле "description"
    user_filter_by_word = get_user_filter_transactions_by_word()

    if isinstance(user_filter_by_word, str):  # если введено слово и нужна фильтрация
        try:
            list_dicts_filtered_by_word = get_dicts_with_pattern(
                filtered_transactions, user_filter_by_word
            )

            if len(list_dicts_filtered_by_word) != 0:  # если получился непустой список
                print("\nРаспечатываю итоговый список транзакций...")
                print(
                    f"Всего банковских операций в выборке: {len(list_dicts_filtered_by_word)}"
                )

                for (
                    dictionary
                ) in (
                    list_dicts_filtered_by_word
                ):  # Проверяем наличие нужных для вывода значений в словарях
                    date_transaction = get_date(dictionary.get("date"))
                    description_transaction = dictionary.get(
                        "description", "Описание отсутствует"
                    )

                    from_value = dictionary.get("from")
                    to_value = dictionary.get("to")

                    # Проверяем, что ключи 'from' и 'to' непустые, прежде чем маскировать номер карты или счета
                    if (
                        from_value
                        and (isinstance(from_value, str))
                        and any(symbol.isdigit() for symbol in from_value)
                    ):
                        from_ = mask_account_card(str(from_value))
                    else:
                        from_ = ""

                    if (
                        to_value
                        and (isinstance(to_value, str))
                        and any(symbol.isdigit() for symbol in to_value)
                    ):
                        to_ = mask_account_card(str(to_value))
                    else:
                        to_ = ""

                    operation_amount = dictionary.get("operationAmount", {})
                    amount_json = operation_amount.get("amount", "Нет данных")
                    currency_json = operation_amount.get("currency", {}).get(
                        "name", "Нет данных"
                    )
                    amount = dictionary.get("amount", "Нет данных")
                    currency = dictionary.get("currency_code", "Нет данных")

                    # Для случая, когда данные получены из json-файла
                    if "operationAmount" in dictionary:
                        print(
                            f"""
                        {date_transaction} {description_transaction}
                        {from_} {to_}
                        {amount_json}: {currency_json}
                        """
                        )

                    # Для случая, когда данные получены из csv или xlsx-файла
                    else:
                        print(
                            f"""
                        {date_transaction} {description_transaction}
                        {from_} {to_}
                        {amount}: {currency}
                        """
                        )
            else:
                return "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"

        except Exception as ex:
            return f"Произошла ошибка {ex}"

    else:  # если фильтровать по слову в описании не нужно, выводим список транзакций, полученных на предыдущем этапе
        try:
            if len(filtered_transactions) != 0:
                print("Распечатываю итоговый список транзакций...")
                print(
                    f"Всего банковских операций в выборке: {len(filtered_transactions)}"
                )
                return filtered_transactions
            else:
                return "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        except Exception as ex:
            return f"Произошла ошибка {ex}"


if __name__ == "__main__":
    main()
