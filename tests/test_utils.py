"""
Тесты для модуля utils.
"""

import json
import os
import tempfile
from unittest.mock import mock_open, patch

import pytest

from src.utils import read_json_file


class TestReadJsonFile:
    """Тесты для функции read_json_file."""

    def test_read_valid_json_file(self):
        """Тест чтения корректного JSON-файла."""
        test_data = [
            {"id": 1, "amount": 100, "currency": "USD"},
            {"id": 2, "amount": 200, "currency": "EUR"}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = read_json_file(temp_path)
            assert result == test_data
            assert isinstance(result, list)
        finally:
            os.unlink(temp_path)

    def test_read_empty_file(self):
        """Тест чтения пустого файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('')
            temp_path = f.name

        try:
            result = read_json_file(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_read_invalid_json(self):
        """Тест чтения некорректного JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{invalid: json}')
            temp_path = f.name

        try:
            result = read_json_file(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_read_not_list(self):
        """Тест чтения JSON, который не является списком."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"key": "value"}, f)
            temp_path = f.name

        try:
            result = read_json_file(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        """Тест при отсутствии файла."""
        result = read_json_file('/non/existent/path.json')
        assert result == []

    @patch('src.utils.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_read_with_mocks(self, mock_file, mock_exists):
        """Тест с использованием Mock."""
        mock_exists.return_value = True
        result = read_json_file('dummy_path.json')
        assert result == []
        mock_exists.assert_called_once_with('dummy_path.json')
