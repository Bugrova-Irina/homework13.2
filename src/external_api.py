import os
from typing import Any

import requests
from dotenv import load_dotenv

from utils import generate_transaction, get_transactions


def get_amount(transaction: dict[str, Any], load_env: bool = True) -> float:
    """Выводит сумму транзакции"""
    amount_transaction = float(transaction["operationAmount"]["amount"])
    currency_transaction = transaction["operationAmount"]["currency"]["code"]

    if currency_transaction == "RUB":
        return amount_transaction

    elif load_env:
        load_dotenv(".env")

        apikey = os.getenv("apikey")

        if not apikey:
            raise ValueError("API ключ не найден. Проверьте файл .env")

        print(f"apikey = {apikey}")
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_transaction}&amount={amount_transaction}"

        headers = {
            "apikey": apikey,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"Ошибка API: {response.status_code}")

        status_code = response.status_code
        result = response.text

        print(response)
        print(response.json())
        print(result)
        print(status_code)

        try:
            json_response = response.json()
            if "result" not in json_response:
                raise ValueError(f"No data for amount {transaction}")

            print(json_response)
            return json_response.get("result", 0)
        except ValueError:
            print("Ошибка при парсинге JSON ответа.")
            return 0.0

    else:
        raise Exception(f"Произошла ошибка")


if __name__ == "__main__":
    result = get_transactions("../homework13.2/data/operations.json")

    transaction_item = generate_transaction(result)

    transaction1 = [next(transaction_item) for i in range(2)][0]

    print(transaction1)
    # print(type(transaction1))

    amount = get_amount(transaction1)
    print(amount)
