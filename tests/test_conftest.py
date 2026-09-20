"""
Общие фикстуры для тестов.
"""

import logging
import sys
from pathlib import Path

import pytest

# Добавляем корень проекта в sys.path, чтобы импортировать src.*
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def clean_loggers():
    """
    Перед и после каждого теста удаляет handlers у логеров masks и utils,
    чтобы setup_logger создал их заново уже с tmp-путём.
    """
    for name in ("masks", "utils"):
        lg = logging.getLogger(name)
        for handler in lg.handlers[:]:
            handler.close()
            lg.removeHandler(handler)

    yield

    for name in ("masks", "utils"):
        lg = logging.getLogger(name)
        for handler in lg.handlers[:]:
            handler.close()
            lg.removeHandler(handler)


@pytest.fixture(autouse=True)
def logs_in_tmp(tmp_path, monkeypatch):
    """
    Перенаправляет папку logs в tmp_path для каждого теста.
    Возвращает путь к временной папке logs.
    """
    import logger as logger_module

    tmp_logs = tmp_path / "logs"
    tmp_logs.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(logger_module, "LOG_DIR", str(tmp_logs))
    yield tmp_logs
