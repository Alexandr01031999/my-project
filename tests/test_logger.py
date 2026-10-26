"""
Тесты для модуля logger.py.
"""

import logging
import os

import pytest

from logger import LOG_DIR, setup_logger


@pytest.fixture(autouse=True)
def clean_logs_dir():
    """Убирает ранее созданные handlers и чистит папку логов перед каждым тестом."""
    yield
    for name in ("masks", "utils", "test_logger_unique"):
        lg = logging.getLogger(name)
        for handler in lg.handlers[:]:
            handler.close()
            lg.removeHandler(handler)


def test_setup_logger_returns_logger():
    logger = setup_logger("test_logger_unique")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger_unique"


def test_setup_logger_level_is_debug():
    logger = setup_logger("test_logger_unique")
    assert logger.level == logging.DEBUG


def test_setup_logger_has_file_handler():
    logger = setup_logger("test_logger_unique")
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)


def test_setup_logger_handler_level_and_formatter():
    logger = setup_logger("test_logger_unique")
    handler = logger.handlers[0]

    expected_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert handler.formatter is not None
    assert handler.formatter._fmt == expected_fmt


def test_setup_logger_creates_log_file():
    logger = setup_logger("test_logger_unique")
    logger.info("test message")
    for handler in logger.handlers:
        handler.flush()

    log_file = os.path.join(LOG_DIR, "test_logger_unique.log")
    assert os.path.exists(log_file)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "test message" in content
    assert "INFO" in content
    assert "test_logger_unique" in content


def test_setup_logger_does_not_duplicate_handlers():
    logger1 = setup_logger("test_logger_unique")
    handlers_count = len(logger1.handlers)
    logger2 = setup_logger("test_logger_unique")
    assert len(logger2.handlers) == handlers_count
