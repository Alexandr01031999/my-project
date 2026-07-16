# Изменения
"""Модуль для маскировки номеров банковских карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Формат вывода: XXXX XX** **** XXXX
    Видны первые 6 цифр и последние 4 цифры.

    Аргументы:
        card_number: Номер карты в виде строки из 16 цифр.

    Возвращает:
        Замаскированный номер карты.

    Пример:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    first_six = card_number[:6]
    last_four = card_number[-4:]

    masked = f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"

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
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")  # Изменено на "минимум"

    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    last_four = account_number[-4:]

    return f"**{last_four}"
