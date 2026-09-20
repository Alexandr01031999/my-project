"""
Модуль с утилитами для работы с JSON-файлами.
"""

import json
import os
from typing import Any, Dict, List

from logger import setup_logger

logger = setup_logger("utils")


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными транзакций.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными транзакций.
        Возвращает пустой список, если файл пустой,
        содержит не список или не найден.
    """
    if not os.path.exists(file_path):
        logger.error("Файл не найден: %s", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.error("Данные в файле %s не являются списком", file_path)
            return []

        logger.info("Файл %s успешно прочитан, записей: %d", file_path, len(data))
        return data

    except (json.JSONDecodeError, ValueError) as e:
        logger.error("Ошибка чтения JSON из файла %s: %s", file_path, e)
        return []
