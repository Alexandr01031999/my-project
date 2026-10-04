"""
Модуль настройки логирования для проекта.
"""

import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    """
    Создаёт и настраивает логер с записью в файл logs/<name>.log.

    Формат записи: метка времени - название модуля - уровень - сообщение.
    Файл перезаписывается при каждом запуске приложения.

    Args:
        name (str): Имя логера (обычно имя модуля).

    Returns:
        logging.Logger: Настроенный логер.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ВАЖНО: LOG_DIR читается здесь, а не в момент импорта
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, f"{name}.log"),
        mode="w",
        encoding="utf-8",
    )

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)

    return logger
