"""
Тесты для модуля masks.py.
"""

import logging

import pytest

from masks import get_mask_account, get_mask_card_number


# ---------- get_mask_card_number ----------

def test_get_mask_card_number_ok():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_with_spaces():
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


def test_get_mask_card_number_with_dashes():
    assert get_mask_card_number("7000-7922-8960-6361") == "7000 79** **** 6361"


def test_get_mask_card_number_too_short():
    with pytest.raises(ValueError, match="16 цифр"):
        get_mask_card_number("1234")


def test_get_mask_card_number_too_long():
    with pytest.raises(ValueError, match="16 цифр"):
        get_mask_card_number("12345678901234567")


def test_get_mask_card_number_empty():
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_card_number_logs_success(caplog):
    with caplog.at_level(logging.INFO, logger="masks"):
        get_mask_card_number("7000792289606361")

    assert "Номер карты успешно замаскирован" in caplog.text
    assert "INFO" in caplog.text


def test_get_mask_card_number_logs_error(caplog):
    with caplog.at_level(logging.ERROR, logger="masks"):
        with pytest.raises(ValueError):
            get_mask_card_number("1234")

    assert "Некорректный номер карты" in caplog.text
    assert "ERROR" in caplog.text


# ---------- get_mask_account ----------

def test_get_mask_account_ok():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_min_length():
    assert get_mask_account("1234") == "**1234"


def test_get_mask_account_with_dashes():
    assert get_mask_account("7365-4108-4301-3587-4305") == "**4305"


def test_get_mask_account_too_short():
    with pytest.raises(ValueError, match="минимум 4 цифры"):
        get_mask_account("123")


def test_get_mask_account_empty():
    with pytest.raises(ValueError):
        get_mask_account("")


def test_get_mask_account_logs_success(caplog):
    with caplog.at_level(logging.INFO, logger="masks"):
        get_mask_account("73654108430135874305")

    assert "Номер счета успешно замаскирован" in caplog.text
    assert "INFO" in caplog.text


def test_get_mask_account_logs_error(caplog):
    with caplog.at_level(logging.ERROR, logger="masks"):
        with pytest.raises(ValueError):
            get_mask_account("12")

    assert "Некорректный номер счета" in caplog.text
    assert "ERROR" in caplog.text
