# Фейковые данные для тестов
FAKE_TRANSACTIONS = [
    {
        "date": "01.01.2024",
        "description": "Перевод организации",
        "state": "EXECUTED",
        "operationAmount": {"amount": "1000", "currency": {"code": "RUB", "name": "руб."}},
        "from": "MasterCard 1234 5678 9012 3456",
        "to": "Счет 98765432101234567890"
    },
    {
        "date": "02.01.2024",
        "description": "Открытие вклада",
        "state": "CANCELED",
        "operationAmount": {"amount": "500", "currency": {"code": "USD", "name": "USD"}},
        "to": "Счет 11112222333344445555"
    }
]


@pytest.fixture(autouse=True)
def mock_load_transactions(monkeypatch):
    """Автоматически подменяем загрузку файлов фейковыми данными."""
    monkeypatch.setattr("main.load_transactions", lambda _: FAKE_TRANSACTIONS)


def test_main_success_flow(monkeypatch, capsys):
    """Тестируем успешный сценарий прохода по меню."""
    # 1 - JSON, EXECUTED - статус, нет - сортировка, нет - рубли, нет - поиск
    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert "Привет! Добро пожаловать" in captured.out
    assert "Для обработки выбран JSON-файл" in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out
    # Проверяем, что вывод отформатирован верно (есть маска)
    assert "Сумма: 1000 руб." in captured.out


def test_main_invalid_status(monkeypatch, capsys):
    """Тестируем защиту от неверного ввода статуса."""
    # Вводим неверный статус "test", потом правильный "CANCELED"
    inputs = iter(["1", "test", "CANCELED", "нет", "нет", "нет"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert 'Статус операции "TEST" недоступен.' in captured.out
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured.out


def test_main_sorting_and_rub_filter(monkeypatch, capsys):
    """Тестируем сортировку и фильтрацию по рублям."""
    # Сортировать (да) -> по убыванию -> Только рубли (да)
    inputs = iter(["1", "EXECUTED", "да", "по убыванию", "да", "нет"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert "Распечатываю итоговый список транзакций" in captured.out
    # Так как у нас только 1 RUB транзакция, выведется 1
    assert "Всего банковских операций в выборке: 1" in captured.out


def test_main_invalid_menu(monkeypatch, capsys):
    """Тестируем неверный пункт меню."""
    inputs = iter(["9"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    main()
    captured = capsys.readouterr()

    assert "Неверный пункт меню." in captured.out
