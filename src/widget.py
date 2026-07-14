"""
Модуль для работы с маскировкой банковских карт и счетов, а также форматированием дат.
"""

from datetime import datetime
from src.masks import get_mask_card_number, get_mask_account  # Импортируем из первого файла


def mask_account_card(account_card: str) -> str:
    """Маскирует номер карты или счета в строке."""
    parts = account_card.split()

    if not parts:
        return account_card

    number = parts[-1]

    if not number.isdigit():
        return account_card

    if len(number) == 16:
        masked_number = get_mask_card_number(number)
    elif len(number) == 20:
        masked_number = get_mask_account(number)
    else:
        return account_card

    return " ".join(parts[:-1] + [masked_number])


def get_date(date_string: str) -> str:
    """Преобразует строку с датой в формат ДД.ММ.ГГГГ."""
    try:
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError, AttributeError):
        return date_stringaaa