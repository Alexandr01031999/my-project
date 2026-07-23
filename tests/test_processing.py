"""
Тесты для модуля processing.
"""

import pytest
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default():
    """Тест фильтрации с параметром по умолчанию 'EXECUTED'."""
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(data)
    expected = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    assert result == expected


def test_filter_by_state_canceled():
    """Тест фильтрации со статусом 'CANCELED'."""
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(data, 'CANCELED')
    expected = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    assert result == expected


def test_filter_by_state_empty():
    """Тест фильтрации с пустым списком."""
    assert filter_by_state([]) == []


def test_filter_by_state_no_matches():
    """Тест фильтрации когда нет совпадений."""
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    result = filter_by_state(data, 'CANCELED')
    assert result == []


def test_sort_by_date_descending():
    """Тест сортировки по убыванию (по умолчанию)."""
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = sort_by_date(data)
    expected = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    assert result == expected


def test_sort_by_date_ascending():
    """Тест сортировки по возрастанию."""
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = sort_by_date(data, False)
    expected = [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]
    assert result == expected


def test_sort_by_date_empty():
    """Тест сортировки пустого списка."""
    assert sort_by_date([]) == []


def test_sort_by_date_same_date():
    """Тест сортировки когда даты одинаковые."""
    data = [
        {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'}
    ]
    result = sort_by_date(data)
    assert len(result) == 2
    # Порядок может быть любым при одинаковых датах
    assert {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'} in result
    assert {'id': 2, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00'} in result