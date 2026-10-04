"""Тесты для модуля widget."""

import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции маскировки карты или счета."""

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
            ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
            ("Maestro 123456789012", "Maestro 1234 56** **** 9012"),
            ("Счет 12345678901234567890", "Счет **7890"),
            ("Счет 9876543210", "Счет **3210"),
            ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),
            ("MIR 1234567890123456", "MIR 1234 56** **** 3456"),
            ("UnionPay 1234567890123456", "UnionPay 1234 56** **** 3456"),
        ],
    )
    def test_valid_card_account_masking(self, input_str: str, expected: str) -> None:
        """Тест корректной маскировки различных типов карт и счетов."""
        assert mask_account_card(input_str) == expected

    @pytest.mark.parametrize(
        "input_str",
        [
            "",
            "  ",
            "Visa",
            "Счет",
            "InvalidCard 123",
        ],
    )
    def test_invalid_inputs(self, input_str: str) -> None:
        """Тест обработки некорректных входных данных."""
        with pytest.raises(ValueError):
            mask_account_card(input_str)

    def test_multiple_spaces_in_card_type(self) -> None:
        """Тест обработки нескольких пробелов в названии карты."""
        result = mask_account_card("Visa   Classic   1234567890123456")
        assert result == "Visa Classic 1234 56** **** 3456"

    def test_card_without_type(self) -> None:
        """Тест маскировки карты без указания типа."""
        result = mask_account_card("1234567890123456")
        assert result == "1234 56** **** 3456"


class TestGetDate:
    """Тесты для функции преобразования даты."""

    @pytest.mark.parametrize(
        "date_str, expected",
        [
            ("2023-10-01T12:00:00", "01.10.2023"),
            ("2023-12-25T23:59:59", "25.12.2023"),
            ("2024-01-01T00:00:00", "01.01.2024"),
            ("2022-03-15T08:30:00", "15.03.2022"),
            ("2023-06-07T18:45:22", "07.06.2023"),
        ],
    )
    def test_valid_date_formats(self, date_str: str, expected: str) -> None:
        """Тест преобразования валидных форматов даты."""
        assert get_date(date_str) == expected

    @pytest.mark.parametrize(
        "date_str",
        [
            "",
            "  ",
            "2023/10/01",
            "01-10-2023",
            "2023-10-01T",
            "invalid-date",
        ],
    )
    def test_invalid_date_formats(self, date_str: str) -> None:
        """Тест обработки невалидных форматов даты."""
        with pytest.raises(ValueError):
            get_date(date_str)

    def test_date_with_milliseconds(self) -> None:
        """Тест преобразования даты с миллисекундами."""
        result = get_date("2023-10-01T12:00:00.123456")
        assert result == "01.10.2023"

    def test_date_with_timezone(self) -> None:
        """Тест преобразования даты с часовым поясом."""
        result = get_date("2023-10-01T12:00:00+03:00")
        assert result == "01.10.2023"

    def test_date_with_microseconds(self) -> None:
        """Тест преобразования даты с микросекундами."""
        result = get_date("2023-12-25T23:59:59.999999")
        assert result == "25.12.2023"
