from src.operations import count_operations_by_category


def test_count_categories() -> None:
    data = [
        {"description": "Перевод"},
        {"description": "Перевод"},
        {"description": "Вклад"},
    ]
    result = count_operations_by_category(data, ["Перевод", "Вклад", "Прочее"])
    assert result == {"Перевод": 2, "Вклад": 1, "Прочее": 0}
