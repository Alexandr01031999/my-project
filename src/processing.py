"""
Модуль для обработки данных банковских операций.
Содержит функции для фильтрации по статусу и сортировки по дате.
"""

from typing import List, Dict, Optional


def filter_by_state(data: List[Dict[str, str | int]], state: str = 'EXECUTED') -> List[Dict[str, str | int]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data (List[Dict[str, str | int]]): Список словарей с данными операций.
            Каждый словарь должен содержать ключи 'id', 'state', 'date'.
        state (str): Значение для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        List[Dict[str, str | int]]: Новый список словарей, содержащий только те записи,
            у которых ключ 'state' соответствует указанному значению.

    Examples:
        >>> transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> filter_by_state(transactions)
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict[str, str | int]], descending: bool = True) -> List[Dict[str, str | int]]:
    """
    Сортирует список словарей по дате.

    Args:
        data (List[Dict[str, str | int]]): Список словарей с данными операций.
            Каждый словарь должен содержать ключ 'date' с датой в формате ISO.
        descending (bool): Порядок сортировки.
            True - по убыванию (сначала новые), False - по возрастанию (сначала старые).
            По умолчанию True.

    Returns:
        List[Dict[str, str | int]]: Новый список словарей, отсортированный по дате.

    Examples:
        >>> transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> sort_by_date(transactions)
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    """
    return sorted(data, key=lambda x: x.get('date', ''), reverse=descending)