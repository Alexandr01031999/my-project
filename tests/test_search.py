from src.search import search_transactions


def test_search_case_insensitive() -> None:
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    assert len(search_transactions(data, "ПЕРЕВОД")) == 1


def test_search_special_chars() -> None:
    data = [{"description": "Оплата 100.50"}]
    assert len(search_transactions(data, "100.50")) == 1


def test_search_empty() -> None:
    assert search_transactions([{"description": "x"}], "") == []
