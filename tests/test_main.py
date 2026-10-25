import pytest
import json
import os
import shutil
from src.main import main


@pytest.fixture(autouse=True)
def setup_dummy_files():
    """Создает временную папку data с файлами для тестов и удаляет после."""
    os.makedirs("data", exist_ok=True)

    # Фейковые транзакции (с разными статусами и валютами)
    fake_transactions = [
        {
            "date": "01.01.2024",
            "description": "Перевод организации",
            "state": "EXECUTED",
            "operationAmount": {"amount": "1000", "currency": {"code": "RUB", "name": "руб."}},
            "from": "Счет 1234",
            "to": "Счет 5678"
        },
        {
            "date": "02.01.2024",
            "description": "Открытие вклада",
            "state": "CANCELED",
            "operationAmount": {"amount": "500", "currency": {"code": "USD", "name": "USD"}},
            "from": "",
            "to": "Счет 9999"
        }
    ]

    # Записываем данные в JSON файл, который ищет программа
    with open("data/transactions.json", "w", encoding="utf-8") as f:
        json.dump(fake_transactions, f, ensure_ascii=False)

    # Если программа тестирует CSV, можно создать и его
    with open("data/transactions.csv", "w", encoding="utf-8") as f:
        f.write("date,description,state\n01.01.2024,Test,EXECUTED\n")

    yield  # Ждем, пока выполнятся тесты

    # Убираем за собой (удаляем папку data, чтобы не мусорить в проекте)
    if os.path.exists("data"):
        shutil.rmtree("data")


def test_main_success_flow(monkeypatch, capsys):
    """Тестируем успешный сценарий прохода по меню."""
    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert "Привет! Добро пожаловать" in captured.out
    assert "Для обработки выбран JSON-файл" in captured.out
    assert "Распечатываю итоговый список транзакций" in captured.out


def test_main_invalid_status(monkeypatch, capsys):
    """Тестируем защиту от неверного ввода статуса."""
    inputs = iter(["1", "test", "CANCELED", "нет", "нет", "нет"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert 'Статус операции "TEST" недоступен.' in captured.out
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured.out


def test_main_sorting_and_rub_filter(monkeypatch, capsys):
    """Тестируем ветки с сортировкой и фильтрацией по рублям."""
    inputs = iter(["1", "EXECUTED", "да", "по убыванию", "да", "нет"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert "Распечатываю итоговый список транзакций" in captured.out


def test_main_invalid_menu(monkeypatch, capsys):
    """Тестируем неверный пункт меню."""
    inputs = iter(["9"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert "Неверный пункт меню." in captured.out

