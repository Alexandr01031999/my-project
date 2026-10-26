"""
Тесты для модуля utils.py.
"""

import json
import logging

import pytest

from utils import read_json_file


@pytest.fixture
def valid_json_file(tmp_path):
    path = tmp_path / "valid.json"
    data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@pytest.fixture
def invalid_json_file(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("{not valid json", encoding="utf-8")
    return str(path)


@pytest.fixture
def non_list_json_file(tmp_path):
    path = tmp_path / "dict.json"
    path.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    return str(path)


# ---------- базовая логика ----------

def test_read_json_file_ok(valid_json_file):
    result = read_json_file(valid_json_file)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_read_json_file_not_found():
    result = read_json_file("nonexistent_file.json")
    assert result == []


def test_read_json_file_invalid_json(invalid_json_file):
    result = read_json_file(invalid_json_file)
    assert result == []


def test_read_json_file_not_a_list(non_list_json_file):
    result = read_json_file(non_list_json_file)
    assert result == []


# ---------- логирование ----------
# Не указываем logger="utils", чтобы не зависеть от имени логера
# (utils или src.utils — оба варианта перехватятся).

def test_read_json_file_logs_success(caplog, valid_json_file):
    with caplog.at_level(logging.INFO):
        read_json_file(valid_json_file)

    assert "успешно прочитан" in caplog.text
    assert any(rec.levelname == "INFO" for rec in caplog.records)


def test_read_json_file_logs_error_not_found(caplog):
    with caplog.at_level(logging.ERROR):
        read_json_file("nonexistent_file.json")

    assert "Файл не найден" in caplog.text
    assert any(rec.levelname == "ERROR" for rec in caplog.records)


def test_read_json_file_logs_error_invalid(caplog, invalid_json_file):
    with caplog.at_level(logging.ERROR):
        read_json_file(invalid_json_file)

    assert "Ошибка чтения JSON" in caplog.text
    assert any(rec.levelname == "ERROR" for rec in caplog.records)


def test_read_json_file_logs_error_not_list(caplog, non_list_json_file):
    with caplog.at_level(logging.ERROR):
        read_json_file(non_list_json_file)

    assert "не являются списком" in caplog.text
    assert any(rec.levelname == "ERROR" for rec in caplog.records)
