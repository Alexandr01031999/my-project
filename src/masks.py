"""
Модуль для маскирования номеров карт и счетов.
"""

from logger import setup_logger

logger = setup_logger("masks")


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты.

    Формат вывода: XXXX XX** **** XXXX
    Видны первые 6 и последние 4 цифры.

    Аргументы:
        card_number: Номер карты в виде строки из 16 цифр.

    Возвращает:
        Замаскированный номер карты.

    Пример:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    cleaned = "".join(filter(str.isdigit, card_number))

    if len(cleaned) != 16:
        logger.error(
            "Некорректный номер карты: ожидалось 16 цифр, получено %d",
            len(cleaned),
        )
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    masked = f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
    logger.info("Номер карты успешно замаскирован")
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Формат вывода: **XXXX
    Видны только последние 4 цифры.

    Аргументы:
        account_number: Номер счета в виде строки (минимум 4 цифры).

    Возвращает:
        Замаскированный номер счета.

    Пример:
        >>> get_mask_account("73654108430135874305")
        '**4305'
    """
    cleaned = "".join(filter(str.isdigit, account_number))

    if len(cleaned) < 4:
        logger.error(
            "Некорректный номер счета: минимум 4 цифры, получено %d",
            len(cleaned),
        )
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    masked = f"**{cleaned[-4:]}"
    logger.info("Номер счета успешно замаскирован")
    return masked
