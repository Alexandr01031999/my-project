"""
Тесты для декоратора log.
"""

import os
import tempfile
from typing import Any

import pytest

from decorators import log


def test_log_to_console_success(capsys: Any) -> None:
    """Тест логирования успешного выполнения в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(3, 5)
    assert result == 8

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_console_error(capsys: Any) -> None:
    """Тест логирования ошибки в консоль."""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


def test_log_to_file_success() -> None:
    """Тест логирования успешного выполнения в файл."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp:
        tmp_path = tmp.name

    try:
        @log(filename=tmp_path)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 6)
        assert result == 24

        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "multiply ok" in content
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_log_to_file_error() -> None:
    """Тест логирования ошибки в файл."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp:
        tmp_path = tmp.name

    try:
        @log(filename=tmp_path)
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}" in content
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_log_with_kwargs(capsys: Any) -> None:
    """Тест логирования с именованными аргументами."""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"

    captured = capsys.readouterr()
    assert "greet ok" in captured.out


def test_log_with_multiple_calls(capsys: Any) -> None:
    """Тест множественных вызовов декорированной функции."""

    @log()
    def square(x: int) -> int:
        return x ** 2

    for i in range(3):
        result = square(i)
        assert result == i ** 2

    captured = capsys.readouterr()
    assert captured.out.count("square ok") == 3


def test_log_preserves_function_metadata() -> None:
    """Тест сохранения метаданных функции."""

    @log()
    def test_func(x: int) -> int:
        """Тестовая функция."""
        return x * 2

    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == "Тестовая функция."


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 7, 2),
])
def test_log_with_parametrize(capsys: Any, a: int, b: int, expected: int) -> None:
    """Параметризованный тест декоратора."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(a, b)
    assert result == expected

    captured = capsys.readouterr()
    assert "add ok" in captured.out
