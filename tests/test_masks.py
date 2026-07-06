"""Тесты для модуля masks."""

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тестирует функцию маскировки номера карты."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    print("✅ Тест маскировки карты пройден")


def test_get_mask_account() -> None:
    """Тестирует функцию маскировки номера счета."""
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("1234567890") == "**7890"
    print("✅ Тест маскировки счета пройден")


def test_get_mask_card_number_errors() -> None:
    """Тестирует обработку ошибок для номера карты."""
    # Короткий номер
    try:
        get_mask_card_number("123")
        print("❌ Ошибка: должна быть ошибка для короткого номера")
    except ValueError as e:
        assert str(e) == "Номер карты должен содержать ровно 16 цифр"
        print("✅ Тест обработки ошибки (короткий номер) пройден")

    # Нецифровой номер
    try:
        get_mask_card_number("123456789012345a")
        print("❌ Ошибка: должна быть ошибка для нецифрового номера")
    except ValueError as e:
        assert str(e) == "Номер карты должен содержать только цифры"
        print("✅ Тест обработки ошибки (нецифровой номер) пройден")


def test_get_mask_account_errors() -> None:
    """Тестирует обработку ошибок для номера счета."""
    # Короткий счет
    try:
        get_mask_account("123")
        print("❌ Ошибка: должна быть ошибка для короткого счета")
    except ValueError as e:
        assert str(e) == "Номер счета должен содержать минимум 4 цифры"  # Исправлено!
        print("✅ Тест обработки ошибки (короткий счет) пройден")

    # Нецифровой счет
    try:
        get_mask_account("12345a67890")
        print("❌ Ошибка: должна быть ошибка для нецифрового счета")
    except ValueError as e:
        assert str(e) == "Номер счета должен содержать только цифры"
        print("✅ Тест обработки ошибки (нецифровой счет) пройден")


if __name__ == "__main__":
    test_get_mask_card_number()
    test_get_mask_account()
    test_get_mask_card_number_errors()
    test_get_mask_account_errors()
    print("\n✅ Все тесты пройдены успешно!")
