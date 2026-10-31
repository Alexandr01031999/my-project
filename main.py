import csv
import json
import openpyxl

from datetime import datetime
from pathlib import Path
from typing import Any

# Импортируем правильные функции из твоего src/masks.py
from src.masks import get_mask_account, get_mask_card_number
from src.operations import count_operations_by_category
from src.search import search_transactions

STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def mask_account_card(data: str) -> str:
    """Обертка: определяет, карта это или счет, и вызывает нужную функцию.
    Если номер нестандартный (не 16 цифр для карты), возвращает строку как есть.
    """
    if not data or data == "None":
        return ""

    if data.startswith("Счет"):
        account_number = data.replace("Счет", "").strip()
        try:
            return f"Счет {get_mask_account(account_number)}"
        except ValueError:
            return data  # если номер счета некорректный — возвращаем как есть

    # Иначе это карта — пробуем замаскировать
    try:
        return get_mask_card_number(data)
    except ValueError:
        return data  # если не 16 цифр — возвращаем как есть (не падаем)


def load_transactions(path: str) -> list[dict[str, Any]]:
    """Загружает транзакции из файла."""
    file_path = Path(path)
    if not file_path.exists():
        return []

    if file_path.suffix == ".json":
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    elif file_path.suffix == ".csv":
        with file_path.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    elif file_path.suffix == ".xlsx":
        import openpyxl
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] is None:
                continue
            transaction = dict(zip(headers, row))
            data.append(transaction)
        return data
    return []


def filter_by_status(data: list[dict[str, Any]], status: str) -> list[dict[str, Any]]:
    """Фильтрует транзакции по статусу (без учёта регистра)."""
    status_upper = status.upper()
    return [t for t in data if str(t.get("state", "")).upper() == status_upper]


def sort_by_date(data: list[dict[str, Any]], ascending: bool = True) -> list[dict[str, Any]]:
    """Сортирует транзакции по дате (поддерживает ISO и DD.MM.YYYY)."""
    def parse_date(t: dict[str, Any]) -> datetime:
        raw = str(t.get("date", ""))
        try:
            # Пробуем ISO-формат (как в CSV/XLSX)
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            try:
                # Пробуем формат ДД.ММ.ГГГГ (как в JSON)
                return datetime.strptime(raw, "%d.%m.%Y")
            except ValueError:
                return datetime.min

    return sorted(data, key=parse_date, reverse=not ascending)


def filter_rub_only(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Оставляет только рублёвые транзакции (поддерживает JSON и CSV/XLSX)."""
    result = []
    for t in data:
        # Пробуем достать код валюты из вложенной структуры (JSON)
        code = (
            t.get("operationAmount", {})
            .get("currency", {})
            .get("code", "")
        )
        # Если не нашли — пробуем плоское поле (CSV/XLSX)
        if not code:
            code = t.get("currency_code", "")

        if str(code).upper() == "RUB":
            result.append(t)
    return result


def format_transaction(t: dict[str, Any]) -> str:
    """Форматирует транзакцию (поддерживает JSON и CSV/XLSX)."""
    date = str(t.get("date", ""))
    desc = str(t.get("description", ""))

    # --- Сумма и валюта ---
    amount_data = t.get("operationAmount", {}) or {}
    amount = amount_data.get("amount")
    currency = (amount_data.get("currency", {}) or {}).get("name", "")

    # Если пусто — значит формат CSV/XLSX
    if amount is None:
        amount = t.get("amount", "0")
    if not currency:
        currency = t.get("currency_name", "")

    # --- Отправитель / Получатель ---
    from_acc = str(t.get("from", ""))
    to_acc = str(t.get("to", ""))

    lines = [f"{date} {desc}"]

    if from_acc and to_acc:
        lines.append(f"{mask_account_card(from_acc)} -> {mask_account_card(to_acc)}")
    elif to_acc:
        lines.append(mask_account_card(to_acc))
    elif from_acc:
        lines.append(mask_account_card(from_acc))

    lines.append(f"Сумма: {amount} {currency}")
    return "\n".join(lines)


def ask_yes_no(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "нет"):
            return answer == "да"
        print("Пожалуйста, введите 'Да' или 'Нет'.")


def main() -> None:
    """Основная логика проекта."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()

    # Проверь названия файлов в папке data! Я оставил стандартные.
    formats = {
        "1": ("JSON", "data/operations.json"),
        "2": ("CSV", "data/transactions.csv"),
        "3": ("XLSX", "data/transactions_excel.xlsx")
    }

    if choice not in formats:
        print("Неверный пункт меню.")
        return

    fmt, path = formats[choice]
    print(f"Для обработки выбран {fmt}-файл.")
    data = load_transactions(path)

    # Фильтрация по статусу
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().strip().upper()
        if status in STATUSES:
            break
        print(f'Статус операции "{status}" недоступен.')

    filtered = filter_by_status(data, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Сортировка
    if ask_yes_no("Отсортировать операции по дате? Да/Нет\n"):
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        filtered = sort_by_date(filtered, ascending=(order == "по возрастанию"))

    # Только рубли
    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет\n"):
        filtered = filter_rub_only(filtered)

    # Поиск по описанию
    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"):
        word = input("Введите слово для поиска:\n").strip()
        filtered = search_transactions(filtered, word)

        # --- ОТЛАДКА ---
        print(f"DEBUG: Всего загружено: {len(data)}")
        print(f"DEBUG: После статуса: {len(filtered)}")
        if filtered:
            print(f"DEBUG: Первая транзакция: {filtered[0]}")
        # --- КОНЕЦ ОТЛАДКИ ---
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
