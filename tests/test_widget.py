"""
Тесты для модуля widget
"""

from src.widget import mask_account_card, get_date


def test_mask_account_card():
    """Тестирование функции mask_account_card"""
    # Тесты для карт
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
    assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert mask_account_card("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"
    assert mask_account_card("Visa Platinum 8990922113665229") == "Visa Platinum 8990 92** **** 5229"
    assert mask_account_card("Visa Gold 5999414228426353") == "Visa Gold 5999 41** **** 6353"

    # Тесты для счетов
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"
    assert mask_account_card("Счет 35383033474447895560") == "Счет **5560"
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"

    # Тест на некорректный ввод
    assert mask_account_card("Неверный формат") == "Неверный формат"
    assert mask_account_card("Счет 123 456") == "Счет 123 456"

    print("Все тесты mask_account_card пройдены!")


def test_get_date():
    """Тестирование функции get_date"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-12-25T15:30:00") == "25.12.2023"
    assert get_date("2022-01-01T00:00:00.000000") == "01.01.2022"

    print("Все тесты get_date пройдены!")


if __name__ == "__main__":
    test_mask_account_card()
    test_get_date()