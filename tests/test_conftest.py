"""Общие фикстуры для всех тестов."""

import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2023-09-15T10:30:00", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-15T08:45:00", "amount": 300},
        {"id": 4, "state": "CANCELED", "date": "2023-08-01T15:20:00", "amount": 400},
    ]


@pytest.fixture
def sample_card_account_strings():
    """Фикстура с различными строковыми представлениями карт и счетов."""
    return [
        {"input": "Visa 1234567890123456", "expected": "Visa 1234 56** **** 3456"},
        {"input": "MasterCard 9876543210987654", "expected": "MasterCard 9876 54** **** 7654"},
        {"input": "Счет 12345678901234567890", "expected": "Счет **7890"},
        {"input": "Maestro 123456789012", "expected": "Maestro 1234 56** **** 9012"},
    ]
