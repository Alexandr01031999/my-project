"""
Тесты для модуля external_api.
"""

import os
from unittest.mock import patch, MagicMock
import requests
import pytest

from src.external_api import convert_currency_to_rub, _convert_via_api


class TestConvertCurrencyToRub:
    """Тесты для функции convert_currency_to_rub."""

    def test_convert_rub_currency(self):
        """Тест конвертации RUB (без изменения)."""
        transaction = {"amount": 1500.50, "currency": "RUB"}
        result = convert_currency_to_rub(transaction)
        assert result == 1500.50
        assert isinstance(result, float)

    def test_convert_usd_via_api(self):
        """Тест конвертации USD через API."""
        with patch('src.external_api._convert_via_api') as mock_convert:
            mock_convert.return_value = 7500.00
            transaction = {"amount": 100.00, "currency": "USD"}
            result = convert_currency_to_rub(transaction)
            assert result == 7500.00
            mock_convert.assert_called_once_with(100.00, "USD")

    def test_convert_eur_via_api(self):
        """Тест конвертации EUR через API."""
        with patch('src.external_api._convert_via_api') as mock_convert:
            mock_convert.return_value = 8500.00
            transaction = {"amount": 100.00, "currency": "EUR"}
            result = convert_currency_to_rub(transaction)
            assert result == 8500.00
            mock_convert.assert_called_once_with(100.00, "EUR")

    def test_missing_amount(self):
        """Тест при отсутствии поля amount."""
        transaction = {"currency": "USD"}
        with pytest.raises(ValueError, match="поля 'amount' и 'currency'"):
            convert_currency_to_rub(transaction)

    def test_missing_currency(self):
        """Тест при отсутствии поля currency."""
        transaction = {"amount": 100.00}
        with pytest.raises(ValueError, match="поля 'amount' и 'currency'"):
            convert_currency_to_rub(transaction)

    @patch('src.external_api._convert_via_api')
    def test_convert_other_currency(self, mock_convert):
        """Тест конвертации другой валюты (не USD/EUR/RUB)."""
        transaction = {"amount": 100.00, "currency": "GBP"}
        result = convert_currency_to_rub(transaction)
        assert result == 100.00
        mock_convert.assert_not_called()


class TestConvertViaApi:
    """Тесты для функции _convert_via_api."""

    @patch('src.external_api.requests.get')
    @patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
    def test_successful_api_call(self, mock_get):
        """Тест успешного вызова API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": 7500.00
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = _convert_via_api(100.00, "USD")
        assert result == 7500.00

        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_key"},
            params={"to": "RUB", "from": "USD", "amount": 100.00},
            timeout=10
        )

    @patch('src.external_api.requests.get')
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self, mock_get):
        """Тест при отсутствии API ключа."""
        with pytest.raises(RuntimeError, match="API ключ не найден"):
            _convert_via_api(100.00, "USD")
        mock_get.assert_not_called()

    @patch('src.external_api.requests.get')
    @patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
    def test_api_request_exception(self, mock_get):
        """Тест при ошибке сетевого запроса."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        with pytest.raises(RuntimeError, match="Ошибка при запросе к API"):
            _convert_via_api(100.00, "USD")

    @patch('src.external_api.requests.get')
    @patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
    def test_api_unsuccessful_response(self, mock_get):
        """Тест при неуспешном ответе API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "error": {"code": 404, "message": "Not found"}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(RuntimeError, match="Ошибка API"):
            _convert_via_api(100.00, "USD")
