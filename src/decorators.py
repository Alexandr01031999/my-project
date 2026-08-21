"""
Модуль с декораторами для логирования.
"""

import functools
import logging
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.

    Args:
        filename: Имя файла для записи логов. Если не указан, логи выводятся в консоль.

    Returns:
        Декорированная функция.
    """

    def decorator(func: Callable) -> Callable:
        """Внутренний декоратор."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обёртка функции с логированием."""
            # Настройка логгера
            logger = logging.getLogger(func.__name__)

            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8')
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            # Логирование выполнения
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                args_repr = ', '.join(repr(arg) for arg in args)
                kwargs_repr = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())
                inputs = f"({args_repr})" + (f", {{{kwargs_repr}}}" if kwargs_repr else "")
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs}")
                raise
            finally:
                # Удаляем хендлер, чтобы не накапливались
                logger.removeHandler(handler)
                handler.close()

        return wrapper

    return decorator
