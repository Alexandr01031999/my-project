python
"""
Модуль для работы с маскировкой банковских карт и счетов, а также форматированием дат.
"""

from datetime import datetime


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты в виде строки (16 цифр)

    Returns:
        Замаскированный номер карты
    """
    if len(card_number) != 16 or not card_number.isdigit():
        return card_number

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX.

    Args:
        account_number: Номер счета в виде строки

    Returns:
        Замаскированный номер счета
    """
    if len(account_number) < 4:
        return account_number

    return f"**{account_number[-4:]}"


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Args:
        account_info: Строка с типом и номером карты/счета

    Returns:
        Строка с замаскированным номером

    Examples:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    # Разделяем строку на части
    parts = account_info.rsplit(' ', 1)

    if len(parts) != 2:
        # Если ввод не корректный (нет номера или более 2 подстрок)
        return account_info

    name, number = parts[0], parts[1]

    # Проверяем, является ли строка номером счета
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        # Для всех карт используем маскировку карты
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Строка с датой в формате ISO (например, "2024-03-11T02:26:18.671407")

    Returns:
        Строка с датой в формате "ДД.ММ.ГГГГ"

    Examples:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    try:
        # Парсим ISO строку
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        # Если строка не является корректным ISO форматом
        return date_string