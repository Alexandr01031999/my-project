"""Проверка покрытия тестами."""

import os


def test_all_modules_have_tests():
    """Проверка, что для всех модулей есть тесты."""
    src_modules = []
    test_modules = []

    # Получаем список всех модулей в src
    src_path = "src"
    if os.path.exists(src_path):
        for file in os.listdir(src_path):
            if file.endswith(".py") and not file.startswith("__"):
                src_modules.append(file.replace(".py", ""))

    # Получаем список всех тестовых модулей
    test_path = "tests"
    if os.path.exists(test_path):
        for file in os.listdir(test_path):
            if file.startswith("test_") and file.endswith(".py"):
                test_name = file.replace("test_", "").replace(".py", "")
                test_modules.append(test_name)

    # Проверяем, что для каждого модуля есть тест
    missing_tests = set(src_modules) - set(test_modules)
    assert not missing_tests, f"Нет тестов для модулей: {missing_tests}"
