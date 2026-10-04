"""Модуль для работы с виджетами."""

from src.masks import get_mask_account, get_mask_card_number


def _normalize_input(input_str: str) -> tuple:
    """
    Нормализует входную строку и разделяет на тип и номер.

    Аргументы:
        input_str: Входная строка

    Возвращает:
        Кортеж (тип, номер) или (None, номер) если тип не указан

    Raises:
        ValueError: Если входная строка некорректна
    """
    if not input_str or not input_str.strip():
        raise ValueError("Входная строка не может быть пустой")

    # Нормализуем пробелы
    normalized = " ".join(input_str.split())
    parts = normalized.rsplit(" ", 1)

    if len(parts) == 2:
        # Есть и тип, и номер
        card_type, number = parts
        # Проверяем, что номер содержит цифры
        if any(c.isdigit() for c in number):
            return card_type, number
        else:
            # Если номер не содержит цифр, возможно это не номер
            raise ValueError("Неверный формат ввода. Ожидается: 'Тип номер'")
    else:
        # Только номер без типа
        cleaned = "".join(filter(str.isdigit, input_str))
        if cleaned:
            return None, cleaned
        raise ValueError("Неверный формат ввода. Ожидается: 'Тип номер'")


def _clean_number(number: str) -> str:
    """
    Очищает номер от разделителей и проверяет его.

    Аргументы:
        number: Строка с номером

    Возвращает:
        Очищенный номер

    Raises:
        ValueError: Если номер не содержит цифр
    """
    cleaned = "".join(filter(str.isdigit, number))
    if not cleaned:
        raise ValueError("Номер должен содержать цифры")
    return cleaned


def _is_card_type(card_type: str) -> bool:
    """
    Проверяет, является ли тип картой.

    Аргументы:
        card_type: Тип карты/счета

    Возвращает:
        True если это карта, иначе False
    """
    # Если тип не указан, считаем что это карта
    if not card_type:
        return True

    # Если в типе есть слово "Счет" - это счет
    if "счет" in card_type.lower():
        return False

    # Список ключевых слов для карт
    card_keywords = ["visa", "mastercard", "maestro", "mir", "unionpay"]

    # Проверяем, содержится ли ключевое слово в типе
    return any(keyword in card_type.lower() for keyword in card_keywords)


def _mask_card_number(number: str) -> str:
    """
    Маскирует номер карты.

    Аргументы:
        number: Номер карты

    Возвращает:
        Замаскированный номер
    """
    if len(number) >= 16:
        return get_mask_card_number(number)
    elif len(number) >= 12:
        # Для коротких номеров карт (12-15 цифр)
        return f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    else:
        # Слишком короткий номер
        return f"{'*' * (len(number) - 4)}{number[-4:]}"


def mask_account_card(input_str: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Аргументы:
        input_str: Строка вида "Visa 1234567890123456" или "Счет 12345678901234567890"

    Возвращает:
        Замаскированная строка.

    Примеры:
        >>> mask_account_card("Visa 1234567890123456")
        'Visa 1234 56** **** 3456'
        >>> mask_account_card("Счет 12345678901234567890")
        'Счет **7890'
        >>> mask_account_card("1234567890123456")
        '1234 56** **** 3456'
    """
    # Нормализуем входные данные
    card_type, number = _normalize_input(input_str)

    # Очищаем номер
    cleaned_number = _clean_number(number)

    # Определяем тип и маскируем
    is_card = _is_card_type(card_type)

    if is_card:
        # Это карта
        try:
            masked_number = _mask_card_number(cleaned_number)
        except ValueError:
            # Если не получилось как карта, пробуем как счет
            masked_number = get_mask_account(cleaned_number)
    else:
        # Это счет
        masked_number = get_mask_account(cleaned_number)

    # Если тип не указан, возвращаем только маскированный номер
    if not card_type:
        return masked_number

    return f"{card_type} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формат ДД.ММ.ГГГГ.

    Аргументы:
        date_str: Строка с датой в формате ISO

    Возвращает:
        Дата в формате ДД.ММ.ГГГГ

    Примеры:
        >>> get_date("2023-10-01T12:00:00")
        '01.10.2023'
    """
    from datetime import datetime

    if not date_str or not date_str.strip():
        raise ValueError("Пустая строка даты")

    try:
        clean_date = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_date)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        try:
            if "." in date_str:
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError(f"Неверный формат даты: {date_str}")
