import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты для функции маскировки номера карты"""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("1234567890123456", "1234 56** **** 3456"),
            ("0000111122223333", "0000 11** **** 3333"),
            ("9999999999999999", "9999 99** **** 9999"),
        ],
    )
    def test_valid_card_numbers(self, card_number, expected):
        """Тест корректной маскировки валидных номеров карт"""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "card_number",
        [
            "",
            "123",
            "12345678901234567",
            "1234567890123456789",
        ],
    )
    def test_invalid_card_numbers(self, card_number):
        """Тест обработки невалидных номеров карт"""
        with pytest.raises(ValueError):
            get_mask_card_number(card_number)

    def test_card_number_with_spaces(self):
        """Тест маскировки номера карты с пробелами"""
        assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"

    def test_card_number_with_dashes(self):
        """Тест маскировки номера карты с дефисами"""
        assert get_mask_card_number("1234-5678-9012-3456") == "1234 56** **** 3456"


class TestGetMaskAccount:
    """Тесты для функции маскировки номера счета"""

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("12345678901234567890", "**7890"),
            ("98765432109876543210", "**3210"),
            ("1234567890", "**7890"),
            ("11111111111111111111", "**1111"),
        ],
    )
    def test_valid_account_numbers(self, account_number, expected):
        """Тест корректной маскировки валидных номеров счетов"""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize(
        "account_number",
        [
            "",
            "123",
            "12",
            "1",
        ],
    )
    def test_short_account_numbers(self, account_number):
        """Тест обработки слишком коротких номеров счетов"""
        with pytest.raises(ValueError):
            get_mask_account(account_number)

    def test_account_with_spaces(self):
        """Тест маскировки номера счета с пробелами"""
        assert get_mask_account("1234 5678 9012 3456 7890") == "**7890"

    def test_account_with_dashes(self):
        """Тест маскировки номера счета с дефисами"""
        assert get_mask_account("1234-5678-9012-3456-7890") == "**7890"
