"""Модуль для чтения финансовых транзакций из CSV- и Excel-файлов."""

from pathlib import Path
from typing import Any, Union, cast

import pandas as pd

PathLike = Union[str, Path]


def read_transactions_csv(path: PathLike) -> list[dict[str, Any]]:
    """Считывает финансовые транзакции из CSV-файла.

    Args:
        path: Путь к CSV-файлу с транзакциями.

    Returns:
        Список словарей, каждый словарь описывает одну транзакцию.
    """
    dataframe = pd.read_csv(path)
    return cast(list[dict[str, Any]], dataframe.to_dict(orient="records"))


def read_transactions_excel(path: PathLike) -> list[dict[str, Any]]:
    """Считывает финансовые транзакции из Excel-файла (XLSX).

    Args:
        path: Путь к Excel-файлу с транзакциями.

    Returns:
        Список словарей, каждый словарь описывает одну транзакцию.
    """
    dataframe = pd.read_excel(path)
    return cast(list[dict[str, Any]], dataframe.to_dict(orient="records"))
