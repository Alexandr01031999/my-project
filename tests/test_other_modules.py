"""
Тесты для остальных модулей проекта.
"""

import pytest
from src import masks, processing, widget


def test_masks_get_mask_card_number() -> None:
    """Тест маскировки номера карты."""
    result = masks.get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"  # Замените на актуальный формат


def test_masks_get_mask_account_number() -> None:
    """Тест маскировки номера счета."""
    result = masks.get_mask_account_number("12345678901234567890")
    assert result == "**7890"  # Замените на актуальный формат


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
    result = processing.sort_by_date(operations, descending=True)
    assert result[0]["date"] == "2023-02-01"


def test_widget_mask_account_card() -> None:
    """Тест маскировки счета или карты."""
    # Добавьте тесты для widget функций
    pass
