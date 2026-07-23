"""
Модуль для обработки данных банковских операций.
Содержит функции для фильтрации по статусу и сортировки по дате.
"""

from typing import List, Dict, Optional


def filter_by_state(data: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data: Список словарей с данными операций
        state: Значение для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Новый список словарей, содержащий только те записи,
        у которых ключ 'state' соответствует указанному значению.

    Examples:
        >>> transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        ...     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ... ]
        >>> filter_by_state(transactions)
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

        >>> filter_by_state(transactions, 'CANCELED')
        [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Сортирует список словарей по дате.

    Args:
        data: Список словарей с данными операций
        descending: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Новый список словарей, отсортированный по дате.

    Examples:
        >>> transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        ...     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ... ]
        >>> sort_by_date(transactions)
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    """
    return sorted(data, key=lambda x: x.get('date', ''), reverse=descending)