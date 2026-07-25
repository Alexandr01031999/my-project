"""
Тесты для модуля processing.
"""

import pytest
from typing import List, Dict, Union
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default() -> None:
    """Тест фильтрации с параметром по умолчанию 'EXECUTED'."""
    data: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result: List[Dict[str, Union[str, int]]] = filter_by_state(data)
    expected: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    assert result == expected


def test_filter_by_state_canceled() -> None:
    """Тест фильтрации со статусом 'CANCELED'."""
    data: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result: List[Dict[str, Union[str, int]]] = filter_by_state(data, 'CANCELED')
    expected: List[Dict[str, Union[str, int]]] = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    assert result == expected


def test_filter_by_state_empty() -> None:
    """Тест фильтрации с пустым списком."""
    result: List[Dict[str, Union[str, int]]] = filter_by_state([])
    expected: List[Dict[str, Union[str, int]]] = []
    assert result == expected


def test_filter_by_state_no_matches() -> None:
    """Тест фильтрации когда нет совпадений."""
    data: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    result: List[Dict[str, Union[str, int]]] = filter_by_state(data, 'CANCELED')
    expected: List[Dict[str, Union[str, int]]] = []
    assert result == expected


def test_sort_by_date_descending() -> None:
    """Тест сортировки по убыванию (по умолчанию)."""
    data: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result: List[Dict[str, Union[str, int]]] = sort_by_date(data)
    expected: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    assert result == expected


def test_sort_by_date_ascending() -> None:
    """Тест сортировки по возрастанию."""
    data: List[Dict[str, Union[str, int]]] = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result: List[Dict[str, Union[str, int]]] = sort_by_date(data, False)
    expected: List[Dict[str, Union[str, int]]] = [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]
    assert result == expected


def test_sort_by_date_empty() -> None:
    """Тест сортировки пустого списка."""
    result: List[Dict[str, Union[str, int]]] = sort_by_date([])
    expected: List[Dict[str, Union[str, int]]] = []
    assert result == expected


def test_sort_by_date_same_date() -> None:
    """Тест сортировки когда даты одинаковые."""
    data: List[Dict[str, Union[str, int]]] = [
        {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'}
    ]
    result: List[Dict[str, Union[str, int]]] = sort_by_date(data)
    assert len(result) == 2
    # Порядок может быть любым при одинаковых датах
    assert {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'} in result
    assert {'id': 2, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'} in result