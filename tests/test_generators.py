"""
Тесты для модуля generators.
"""

import pytest
from typing import List, Dict, Any, Iterator

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с образцами транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]


# Тесты для filter_by_currency
def test_filter_by_currency_with_usd(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по валюте USD."""
    usd_filter: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions, "USD")
    result: List[Dict[str, Any]] = list(usd_filter)
    assert len(result) == 2
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_with_rub(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по валюте RUB."""
    rub_filter: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions, "RUB")
    result: List[Dict[str, Any]] = list(rub_filter)
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


@pytest.mark.parametrize("currency,expected_count", [
    ("USD", 2),
    ("RUB", 1),
    ("EUR", 0),
])
def test_filter_by_currency_parametrized(
    sample_transactions: List[Dict[str, Any]],
    currency: str,
    expected_count: int
) -> None:
    """Параметризованный тест фильтрации по различным валютам."""
    filtered: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions, currency)
    result: List[Dict[str, Any]] = list(filtered)
    assert len(result) == expected_count


def test_filter_by_currency_empty_list() -> None:
    """Тест фильтрации с пустым списком."""
    empty_filter: Iterator[Dict[str, Any]] = filter_by_currency([], "USD")
    result: List[Dict[str, Any]] = list(empty_filter)
    assert result == []


def test_filter_by_currency_no_matching_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации с отсутствующей валютой."""
    eur_filter: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions, "EUR")
    result: List[Dict[str, Any]] = list(eur_filter)
    assert result == []


def test_filter_by_currency_iterator(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест, что функция возвращает итератор."""
    result: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions, "USD")
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")
    first: Dict[str, Any] = next(result)
    assert first["operationAmount"]["currency"]["code"] == "USD"


# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест получения описаний транзакций."""
    descriptions: List[str] = list(transaction_descriptions(sample_transactions))
    expected: List[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет"
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list() -> None:
    """Тест с пустым списком транзакций."""
    descriptions: List[str] = list(transaction_descriptions([]))
    assert descriptions == []


def test_transaction_descriptions_missing_description() -> None:
    """Тест с отсутствующим описанием."""
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "description": "Test"},
        {"id": 2},  # Нет описания
        {"id": 3, "description": "Test 3"}
    ]
    descriptions: List[str] = list(transaction_descriptions(transactions))
    assert descriptions == ["Test", "", "Test 3"]


def test_transaction_descriptions_generator(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест, что функция является генератором."""
    result: Iterator[str] = transaction_descriptions(sample_transactions)
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")
    first: str = next(result)
    assert first == "Перевод организации"


# Тесты для card_number_generator
def test_card_number_generator_range() -> None:
    """Тест генерации номеров карт в заданном диапазоне."""
    cards: List[str] = list(card_number_generator(1, 5))
    expected: List[str] = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]
    assert cards == expected


def test_card_number_generator_format() -> None:
    """Тест форматирования номеров карт."""
    cards: List[str] = list(card_number_generator(1234, 1234))
    assert cards == ["0000 0000 0000 1234"]


def test_card_number_generator_single() -> None:
    """Тест генерации одного номера."""
    cards: List[str] = list(card_number_generator(9999, 9999))
    assert cards == ["0000 0000 0000 9999"]


@pytest.mark.parametrize("start,stop,expected", [
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    (9999999999999998, 9999999999999999,
     ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    (1000, 1003, ["0000 0000 0000 1000", "0000 0000 0000 1001",
                  "0000 0000 0000 1002", "0000 0000 0000 1003"]),
])
def test_card_number_generator_parametrized(start: int, stop: int, expected: List[str]) -> None:
    """Параметризованный тест генерации номеров карт."""
    cards: List[str] = list(card_number_generator(start, stop))
    assert cards == expected


def test_card_number_generator_invalid_start() -> None:
    """Тест с недопустимым начальным значением."""
    with pytest.raises(ValueError, match="Start must be between 1 and 9999999999999999"):
        list(card_number_generator(0, 10))


def test_card_number_generator_invalid_stop() -> None:
    """Тест с недопустимым конечным значением."""
    with pytest.raises(ValueError, match="Stop must be between 1 and 9999999999999999"):
        list(card_number_generator(1, 10000000000000000))


def test_card_number_generator_start_greater_than_stop() -> None:
    """Тест с начальным значением больше конечного."""
    with pytest.raises(ValueError, match="Start must be less than or equal to stop"):
        list(card_number_generator(10, 1))


def test_card_number_generator_max_range() -> None:
    """Тест с максимальным диапазоном."""
    cards: List[str] = list(card_number_generator(9999999999999999, 9999999999999999))
    assert cards == ["9999 9999 9999 9999"]
