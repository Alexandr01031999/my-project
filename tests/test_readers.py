"""Тесты для модуля src.readers."""

from unittest.mock import MagicMock, patch

import pandas as pd

from src.readers import read_transactions_csv, read_transactions_excel


@patch("src.readers.pd.read_csv")
def test_read_transactions_csv_returns_list_of_dicts(
    mock_read_csv: MagicMock,
) -> None:
    """CSV-функция возвращает список словарей с транзакциями."""
    mock_read_csv.return_value = pd.DataFrame(
        [
            {"id": 1, "amount": 100.0, "currency": "RUB"},
            {"id": 2, "amount": 200.0, "currency": "USD"},
        ]
    )

    result = read_transactions_csv("fake.csv")

    mock_read_csv.assert_called_once_with("fake.csv")
    assert isinstance(result, list)
    assert result == [
        {"id": 1, "amount": 100.0, "currency": "RUB"},
        {"id": 2, "amount": 200.0, "currency": "USD"},
    ]


@patch("src.readers.pd.read_csv")
def test_read_transactions_csv_passes_path_argument(
    mock_read_csv: MagicMock,
) -> None:
    """CSV-функция передаёт путь в pd.read_csv как аргумент."""
    mock_read_csv.return_value = pd.DataFrame()

    read_transactions_csv("/tmp/data.csv")

    mock_read_csv.assert_called_once_with("/tmp/data.csv")


@patch("src.readers.pd.read_excel")
def test_read_transactions_excel_returns_list_of_dicts(
    mock_read_excel: MagicMock,
) -> None:
    """Excel-функция возвращает список словарей с транзакциями."""
    mock_read_excel.return_value = pd.DataFrame(
        [
            {"id": 1, "amount": 300.0, "currency": "EUR"},
        ]
    )

    result = read_transactions_excel("fake.xlsx")

    mock_read_excel.assert_called_once_with("fake.xlsx")
    assert isinstance(result, list)
    assert result == [{"id": 1, "amount": 300.0, "currency": "EUR"}]


@patch("src.readers.pd.read_excel")
def test_read_transactions_excel_passes_path_argument(
    mock_read_excel: MagicMock,
) -> None:
    """Excel-функция передаёт путь в pd.read_excel как аргумент."""
    mock_read_excel.return_value = pd.DataFrame()

    read_transactions_excel("/tmp/data.xlsx")

    mock_read_excel.assert_called_once_with("/tmp/data.xlsx")
