"""
Модуль с декораторами для логирования.
"""

import functools
import logging
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.

    Args:
        filename: Имя файла для записи логов.
            Если не указан, логи выводятся в консоль.

    Returns:
        Декорированная функция.
    """
    def decorator(func: Callable) -> Callable:
        """Внутренний декоратор."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обёртка функции с логированием."""
            logger = logging.getLogger(f"{func.__name__}_{id(wrapper)}")
            logger.setLevel(logging.INFO)
            logger.propagate = False

            # Удаляем старые хендлеры
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
                handler.close()

            # Создаём новый хендлер
            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8', mode='a')
            else:
                handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                # Форматируем позиционные аргументы
                args_str = ', '.join(repr(arg) for arg in args)
                # Запятая нужна всегда, если аргумент ровно один
                if len(args) == 1:
                    args_str += ','

                # Форматируем именованные аргументы
                kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())

                # Собираем inputs
                inputs = f"({args_str})"
                if kwargs_str:
                    inputs += f", {{{kwargs_str}}}"

                logger.error(
                    f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs}"
                )
                raise
            finally:
                # Очищаем хендлеры
                for handler in logger.handlers[:]:
                    logger.removeHandler(handler)
                    handler.close()

        return wrapper
    return decorator
