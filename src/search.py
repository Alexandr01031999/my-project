import re
from typing import Any

Transaction = dict[str, Any]


def search_transactions(data: list[Transaction], search: str) -> list[Transaction]:
    """Ищет транзакции, в описании которых встречается подстрока `search`.

    Поиск выполняется без учёта регистра с использованием библиотеки re.

    :param data: список словарей с данными о банковских операциях.
    :param search: строка для поиска в поле description.
    :return: список словарей с операциями, у которых в описании
             есть строка, переданная аргументу функции.
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        transaction
        for transaction in data
        if pattern.search(transaction.get("description", ""))
    ]
