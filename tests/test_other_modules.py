"""
Тесты для остальных модулей проекта.
"""

import pytest
from src import masks, processing, widget


def test_masks_get_mask_card_number() -> None:
    """Тест маскировки номера карты."""
    result = masks.get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"


def test_masks_get_mask_account_number() -> None:
    """Тест маскировки номера счета."""
    result = masks.get_mask_account("12345678901234567890")
    assert result == "**7890"


def test_processing_filter_by_state() -> None:
    """Тест фильтрации по статусу."""
    operations = [
        {"state": "EXECUTED", "amount": 100},
        {"state": "CANCELED", "amount": 200},
    ]
    result = processing.filter_by_state(operations, "EXECUTED")
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


def test_processing_sort_by_date() -> None:
    """Тест сортировки по дате."""
    operations = [
        {"date": "2023-01-01", "amount": 100},
        {"date": "2023-02-01", "amount": 200},
    ]
    # По умолчанию (ascending=False) — от новых к старым
    result = processing.sort_by_date(operations)
    assert result[0]["date"] == "2023-02-01"
    assert result[1]["date"] == "2023-01-01"

    # Явно ascending=True — от старых к новым
    result_asc = processing.sort_by_date(operations, ascending=True)
    assert result_asc[0]["date"] == "2023-01-01"
    assert result_asc[1]["date"] == "2023-02-01"


def test_widget_mask_account_card() -> None:
    """Тест маскировки счета или карты."""
    # Заглушка — замените на реальный тест, если функция существует
    pass
