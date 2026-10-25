from collections import Counter
from typing import Any

Transaction = dict[str, Any]


def count_operations_by_category(
    data: list[Transaction], categories: list[str]
) -> dict[str, int]:
    """Считает количество операций по каждой категории из списка `categories`.

    Категория определяется по полю description транзакции.

    :param data: список словарей с данными о банковских операциях.
    :param categories: список категорий операций для подсчёта.
    :return: словарь, где ключи — названия категорий,
             а значения — количество операций в каждой категории.
    """
    counts = Counter(
        transaction.get("description", "")
        for transaction in data
        if transaction.get("description", "") in categories
    )
    # гарантируем, что все запрошенные категории есть в результате (даже с 0)
    return {category: counts.get(category, 0) for category in categories}
