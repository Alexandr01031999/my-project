"""
Модуль для работы с внешним API конвертации валют.
"""

import os
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def convert_currency_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции.
            Должен содержать ключи 'amount' и 'currency'.

    Returns:
        float: Сумма транзакции в рублях.

    Raises:
        ValueError: Если транзакция не содержит необходимых ключей.
    """
    amount = transaction.get('amount')
    currency = transaction.get('currency')

    if amount is None or currency is None:
        raise ValueError("Транзакция должна содержать поля 'amount' и 'currency'")

    # Если валюта уже в рублях
    if currency.upper() == 'RUB':
        return float(amount)

    # Если валюта USD или EUR - конвертируем через API
    if currency.upper() in ['USD', 'EUR']:
        return _convert_via_api(amount, currency)

    # Для других валют возвращаем как есть (или можно добавить логику)
    return float(amount)


def _convert_via_api(amount: float, currency: str) -> float:
    """
    Конвертирует сумму через внешнее API.

    Args:
        amount (float): Сумма для конвертации.
        currency (str): Код валюты (USD или EUR).

    Returns:
        float: Сумма в рублях.

    Raises:
        RuntimeError: Если API недоступно или произошла ошибка.
    """
    api_key = os.getenv('EXCHANGE_RATES_API_KEY')
    if not api_key:
        raise RuntimeError("API ключ не найден в переменных окружения")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {
        "to": "RUB",
        "from": currency.upper(),
        "amount": amount
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get('success'):
            return float(data['result'])

        raise RuntimeError(f"Ошибка API: {data.get('error', 'Неизвестная ошибка')}")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка при запросе к API: {e}")
