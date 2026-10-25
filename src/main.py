import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from src.search import search_transactions
from src.operations import count_operations_by_category

STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def load_transactions(path: str) -> list[dict[str, Any]]:
    """Загружает транзакции из файла (JSON/CSV/XLSX — упрощённо JSON/CSV)."""
    file_path = Path(path)
    if file_path.suffix == ".json":
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    if file_path.suffix == ".csv":
        with file_path.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    return []


def filter_by_status(
    data: list[dict[str, Any]], status: str
) -> list[dict[str, Any]]:
    """Фильтрует транзакции по статусу (без учёта регистра)."""
    status_upper = status.upper()
    return [
        t for t in data if str(t.get("state", "")).upper() == status_upper
    ]


def sort_by_date(
    data: list[dict[str, Any]], ascending: bool = True
) -> list[dict[str, Any]]:
    """Сортирует транзакции по дате (формат DD.MM.YYYY)."""

    def parse_date(t: dict[str, Any]) -> datetime:
        raw = str(t.get("date", ""))
        try:
            return datetime.strptime(raw, "%d.%m.%Y")
        except ValueError:
            return datetime.min

    return sorted(data, key=parse_date, reverse=not ascending)


def filter_rub_only(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Оставляет только рублёвые транзакции (currency == RUB)."""
    return [
        t
        for t in data
        if str(t.get("operationAmount", {}).get("currency", {}).get("code", "")).upper()
        == "RUB"
    ]


def format_transaction(t: dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    date = str(t.get("date", ""))
    desc = str(t.get("description", ""))
    amount_data = t.get("operationAmount", {}) or {}
    amount = amount_data.get("amount", "0")
    currency = (amount_data.get("currency", {}) or {}).get("name", "")
    from_acc = str(t.get("from", ""))
    to_acc = str(t.get("to", ""))
    lines = [f"{date} {desc}"]
    if from_acc:
        lines.append(f"{from_acc} -> {to_acc}" if to_acc else from_acc)
    lines.append(f"Сумма: {amount} {currency}")
    return "\n".join(lines)


def _ask_yes_no(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "нет"):
            return answer == "да"
        print("Пожалуйста, введите 'Да' или 'Нет'.")


def main() -> None:
    """Основная логика проекта: связывает загрузку, фильтрацию и вывод."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()
    formats = {"1": ("JSON", "data/transactions.json"),
               "2": ("CSV", "data/transactions.csv"),
               "3": ("XLSX", "data/transactions.xlsx")}
    if choice not in formats:
        print("Неверный пункт меню.")
        return
    fmt, path = formats[choice]
    print(f"Для обработки выбран {fmt}-файл.")
    data = load_transactions(path)

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().strip().upper()
        if status in STATUSES:
            break
        print(f'Статус операции "{status}" недоступен.')
    filtered = filter_by_status(data, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if _ask_yes_no("Отсортировать операции по дате? Да/Нет\n"):
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        filtered = sort_by_date(filtered, ascending=(order == "по возрастанию"))

    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет\n"):
        filtered = filter_rub_only(filtered)

    if _ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"):
        word = input("Введите слово для поиска:\n").strip()
        filtered = search_transactions(filtered, word)

    print("Распечатываю итоговый список транзакций...")
    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"Всего банковских операций в выборке: {len(filtered)}\n")
    for t in filtered:
        print(format_transaction(t))
        print()


if __name__ == "__main__":
    main()
