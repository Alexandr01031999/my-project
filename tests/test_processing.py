"""Тесты для модуля processing."""

import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции фильтрации по статусу."""

    @pytest.fixture
    def sample_transactions(self):
        return [
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "PENDING", "amount": 200},
            {"id": 3, "state": "EXECUTED", "amount": 300},
            {"id": 4, "state": "CANCELED", "amount": 400},
            {"id": 5, "state": "EXECUTED", "amount": 500},
        ]

    @pytest.mark.parametrize(
        "state, expected_ids",
        [
            ("EXECUTED", [1, 3, 5]),
            ("PENDING", [2]),
            ("CANCELED", [4]),
            ("PROCESSED", []),
        ],
    )
    def test_filter_by_state(self, sample_transactions, state, expected_ids):
        """Тест фильтрации транзакций по статусу."""
        result = filter_by_state(sample_transactions, state)
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids

    def test_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = filter_by_state([], "EXECUTED")
        assert result == []

    def test_missing_state_key(self):
        """Тест обработки словарей без ключа state."""
        transactions = [
            {"id": 1, "amount": 100},
            {"id": 2, "state": "EXECUTED", "amount": 200},
        ]
        result = filter_by_state(transactions, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_case_sensitivity(self):
        """Тест чувствительности к регистру."""
        transactions = [
            {"id": 1, "state": "executed", "amount": 100},
            {"id": 2, "state": "EXECUTED", "amount": 200},
        ]
        result = filter_by_state(transactions, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestSortByDate:
    """Тесты для функции сортировки по дате."""

    @pytest.fixture
    def sample_transactions(self):
        return [
            {"id": 1, "date": "2023-10-15T12:00:00"},
            {"id": 2, "date": "2023-09-01T10:30:00"},
            {"id": 3, "date": "2023-10-01T08:45:00"},
            {"id": 4, "date": "2023-08-15T15:20:00"},
        ]

    def test_sort_descending(self, sample_transactions):
        """Тест сортировки по убыванию (по умолчанию)."""
        result = sort_by_date(sample_transactions)
        expected_order = [1, 3, 2, 4]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    def test_sort_ascending(self, sample_transactions):
        """Тест сортировки по возрастанию."""
        result = sort_by_date(sample_transactions, ascending=True)
        expected_order = [4, 2, 3, 1]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    def test_same_dates(self):
        """Тест сортировки при одинаковых датах."""
        transactions = [
            {"id": 1, "date": "2023-10-01T12:00:00"},
            {"id": 2, "date": "2023-10-01T10:00:00"},
            {"id": 3, "date": "2023-10-01T12:00:00"},
        ]
        result = sort_by_date(transactions)
        result_ids = [item["id"] for item in result]
        # Проверяем, что все элементы на месте
        assert sorted(result_ids) == [1, 2, 3]
        # Первый элемент должен быть с самой поздней датой (1 или 3)
        assert result_ids[0] in [1, 3]
        # Последний элемент должен быть с самой ранней датой (2)
        assert result_ids[-1] == 2

    def test_empty_list(self):
        """Тест сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []

    def test_missing_date_key(self):
        """Тест обработки словарей без ключа date."""
        transactions = [
            {"id": 1, "amount": 100},
            {"id": 2, "date": "2023-10-01", "amount": 200},
        ]
        with pytest.raises(KeyError):
            sort_by_date(transactions)

    def test_invalid_date_format(self):
        """Тест обработки невалидного формата даты."""
        transactions = [
            {"id": 1, "date": "2023-10-01T12:00:00"},
            {"id": 2, "date": "invalid-date"},
        ]
        with pytest.raises(ValueError):
            sort_by_date(transactions)
