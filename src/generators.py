"""
Модуль с генераторами для обработки транзакций.
Содержит функции для фильтрации по валюте, получения описаний и генерации номеров карт.
"""

from typing import Iterator, List, Dict, Any


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD", "RUB")

    Yields:
        Dict[str, Any]: Транзакции с указанной валютой

    Examples:
        >>> transactions = [
        ...     {"operationAmount": {"currency": {"code": "USD"}}},
        ...     {"operationAmount": {"currency": {"code": "RUB"}}}
        ... ]
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> next(usd_transactions)
        {'operationAmount': {'currency': {'code': 'USD'}}}
    """
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except (AttributeError, TypeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор описаний транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        str: Описание каждой транзакции

    Examples:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"}
        ... ]
        >>> descriptions = transaction_descriptions(transactions)
        >>> next(descriptions)
        'Перевод организации'
    """
    for transaction in transactions:
        try:
            yield transaction.get("description", "")
        except (AttributeError, TypeError):
            yield ""


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное значение диапазона (включительно)
        stop: Конечное значение диапазона (включительно)

    Yields:
        str: Номер карты в отформатированном виде

    Examples:
        >>> for card in card_number_generator(1, 3):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003

    Raises:
        ValueError: Если start или stop вне допустимого диапазона
    """
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Start must be between 1 and 9999999999999999")
    if not (1 <= stop <= 9999999999999999):
        raise ValueError("Stop must be between 1 and 9999999999999999")
    if start > stop:
        raise ValueError("Start must be less than or equal to stop")

    for number in range(start, stop + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + \
            f"{number:016d}"[8:12] + " " + f"{number:016d}"[12:16]
