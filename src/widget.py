"""
Модуль для работы с маскировкой банковских карт и счетов, а также форматированием дат.
"""

from datetime import datetime


def mask_account_card(account_card: str) -> str:
    """Маскирует номер карты или счета в строке."""
    # Разделяем строку на части
    parts = account_card.split()

    # Проверяем, что есть хотя бы одна часть
    if not parts:
        return account_card

    # Последняя часть - это номер
    number = parts[-1]

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        return account_card

    # Определяем тип по количеству цифр
    if len(number) == 16:
        # Это номер карты
        masked_number = get_mask_card_number(number)
    elif len(number) == 20:
        # Это номер счета
        masked_number = get_mask_account(number)
    else:
        # Неизвестный формат
        return account_card

    # Собираем строку обратно
    return " ".join(parts[:-1] + [masked_number])


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты."""
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр")
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    first_six = card_number[:6]
    last_four = card_number[-4:]
    masked = f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета."""
    if len(account_number) != 20:
        raise ValueError("Номер счета должен содержать ровно 20 цифр")
    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    return f"**{account_number[-4:]}"


def get_date(date_string: str) -> str:
    """Преобразует строку с датой в формат ДД.ММ.ГГГГ."""
    # Ожидаемый формат: "2024-03-11T18:35:31.123456"
    try:
        # Разбиваем по T и берем первую часть (дата)
        date_part = date_string.split("T")[0]
        # Разбиваем дату по "-"
        year, month, day = date_part.split("-")
        # Возвращаем в формате ДД.ММ.ГГГГ
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError, AttributeError):
        # Если формат не подходит, возвращаем исходную строку
        return date_string