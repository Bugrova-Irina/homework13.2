import json
import re
from collections import Counter
from typing import Any


def get_dicts_with_pattern(dicts_file: str, pattern_str: str) -> list[dict[str, Any]]:
    """Возвращает список словарей, у которых в описании есть заданная строка"""

    with open(dicts_file, encoding="utf-8") as file:
        list_dicts = json.load(file)

    pattern = re.compile(pattern_str)
    filtered_dict = [
        dictionary
        for dictionary in list_dicts
        if dictionary.get("description") is not None
        and pattern.search(dictionary["description"])
    ]

    return filtered_dict


def get_dict_of_categories(dicts_file: str, categories: list[str]) -> dict[str, int]:
    """
    возвращает словарь вида
    {'название категории': 'количество операций в каждой категории'}
    """

    with open(dicts_file, encoding="utf-8") as file:
        list_dicts = json.load(file)

    categories_list = []
    for dictionary in list_dicts:
        if dictionary.get("description") is not None and dictionary["description"] in categories:
            categories_list.append(dictionary["description"])

    counted_categories = dict(Counter(categories_list))
    return counted_categories


if __name__ == "__main__":
    word = "вклада"
    print(get_dicts_with_pattern("../homework13.2/data/operations.json", word))

    categories = ['Перевод организации', 'Перевод с карты на счет', 'Перевод с карты на карту', 'Перевод со счета на счет', 'Открытие вклада']
    print(get_dict_of_categories("../homework13.2/data/operations.json", categories))
