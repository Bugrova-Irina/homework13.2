import json
import logging
import os
import random
from typing import Any

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file_path = os.path.join(log_dir, "utils.log")
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")

file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions(json_path: str) -> list[dict[str, Any]]:
    """Выводит список словарей с данными о финансовых транзакциях"""
    try:
        logger.info(f"Записываем данные в файл {json_path}")
        with open(json_path, "r", encoding="utf-8") as json_file:
            transactions = json.load(json_file)

            return transactions
    except (ValueError, json.JSONDecodeError) as ex:
        logger.error(f"Произошла ошибка {ex}")
        return []


def generate_transaction(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Генерирует транзакцию из списка транзакций"""
    if not transactions:
        logger.error("Список транзакций пуст.")
        raise ValueError("Список транзакций пуст.")

    while True:
        try:
            transaction = random.choice(transactions)
            yield transaction
            logger.info("Генерируем транзакцию")
        except ValueError as e:
            logger.error(f"Некорректные исходные данные {e}")
            return f"Некорректные исходные данные {e}"


# if __name__ == "__main__":
#     result = get_transactions("../homework13.2/data/operations.json")
#     print(result)
#
#     if not result:
#         print("Нет доступных транзакций для итерации")
#     else:
#         transaction_item = generate_transaction(result)
#
#         try:
#             transaction1 = [next(transaction_item) for i in range(2)][0]
#             print(transaction1)
#         except StopIteration:
#             print("Не удалось получить транзакции.")
