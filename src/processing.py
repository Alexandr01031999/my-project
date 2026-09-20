"""Модуль для обработки транзакций."""

from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Аргументы:
        transactions: Список словарей с транзакциями
        state: Статус для фильтрации

    Возвращает:
        Отфильтрованный список транзакций
    """
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], ascending: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Аргументы:
        transactions: Список словарей с ключом 'date'
        ascending: Если True - сортировка по возрастанию, иначе по убыванию

    Возвращает:
        Отсортированный список транзакций
    """

    def get_date(transaction: Dict[str, Any]) -> datetime:
        """Извлекает и парсит дату из транзакции."""
        date_str = transaction.get("date")
        if not date_str:
            raise KeyError("Отсутствует ключ 'date' в транзакции")

        # Пробуем разные форматы даты
        try:
            # Стандартный ISO формат
            return datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
        except ValueError:
            try:
                # Формат с миллисекундами
                return datetime.strptime(str(date_str), "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    # Формат без времени
                    return datetime.strptime(str(date_str), "%Y-%m-%d")
                except ValueError as e:
                    raise ValueError(f"Неверный формат даты: {date_str}") from e

    # Для стабильной сортировки при одинаковых датах
    # Создаем список с индексами для сохранения порядка
    indexed_transactions = list(enumerate(transactions))

    # Сортируем по дате и индексу
    sorted_indexed = sorted(indexed_transactions, key=lambda x: (get_date(x[1]), x[0]), reverse=not ascending)

    # Возвращаем только транзакции
    return [t for _, t in sorted_indexed]
