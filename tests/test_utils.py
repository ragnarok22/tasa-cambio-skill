"""Tests for lambda/utils.py functions."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

# Add lambda directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lambda"))

from utils import (
    get_exchange_rates,
    get_random_exchange_explanation,
    get_random_greeting,
    get_rounded_exchange_rates,
)


class TestGetExchangeRates:
    """Tests for get_exchange_rates function."""

    @patch("utils.requests.get")
    def test_successful_fetch(self, mock_get):
        """Test successful API call returns correct data."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "usd": 123.45,
            "eur": 135.67,
            "mlc": 120.50,
        }
        mock_get.return_value = mock_response

        result = get_exchange_rates()

        assert result == {
            "USD": 123.45,
            "EUR": 135.67,
            "MLC": 120.50,
        }
        mock_get.assert_called_once_with(
            "https://tasa-cambio-cuba.vercel.app/api/exchange-rate", timeout=5
        )

    @patch("utils.requests.get")
    def test_api_timeout(self, mock_get):
        """Test timeout returns None."""
        mock_get.side_effect = requests.Timeout("Connection timeout")

        result = get_exchange_rates()

        assert result is None

    @patch("utils.requests.get")
    def test_api_connection_error(self, mock_get):
        """Test connection error returns None."""
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        result = get_exchange_rates()

        assert result is None

    @patch("utils.requests.get")
    def test_http_error(self, mock_get):
        """Test HTTP error returns None."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = get_exchange_rates()

        assert result is None

    @patch("utils.requests.get")
    def test_invalid_json(self, mock_get):
        """Test invalid JSON returns None."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = get_exchange_rates()

        assert result is None

    @patch("utils.requests.get")
    def test_missing_keys(self, mock_get):
        """Test missing keys in response returns None."""
        mock_response = Mock()
        mock_response.json.return_value = {"usd": 123.45}  # Missing eur and mlc
        mock_get.return_value = mock_response

        result = get_exchange_rates()

        assert result is None


class TestGetRoundedExchangeRates:
    """Tests for get_rounded_exchange_rates function."""

    @patch("utils.get_exchange_rates")
    def test_successful_rounding(self, mock_get_rates):
        """Test successful fetch and rounding."""
        mock_get_rates.return_value = {
            "USD": 123.456,
            "EUR": 135.678,
            "MLC": 120.501,
        }

        result = get_rounded_exchange_rates()

        assert result == {
            "USD": 123.46,
            "EUR": 135.68,
            "MLC": 120.5,
        }

    @patch("utils.get_exchange_rates")
    def test_api_failure(self, mock_get_rates):
        """Test returns None when API fails."""
        mock_get_rates.return_value = None

        result = get_rounded_exchange_rates()

        assert result is None


class TestGetRandomGreeting:
    """Tests for get_random_greeting function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        result = get_random_greeting()

        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_valid_greeting(self):
        """Test that function returns one of the predefined greetings."""
        valid_greetings = [
            "Asere que bolá? Los precios están mandáo",
            "En talla asere",
            "Ufff, los precios están por las nubes",
            "Saludos broder",
        ]

        result = get_random_greeting()

        assert result in valid_greetings

    def test_randomness(self):
        """Test that function can return different greetings."""
        results = {get_random_greeting() for _ in range(50)}

        # With 50 calls, we should get at least 2 different greetings
        assert len(results) >= 2


class TestGetRandomExchangeExplanation:
    """Tests for get_random_exchange_explanation function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        result = get_random_exchange_explanation()

        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_valid_explanation(self):
        """Test that function returns one of the predefined explanations."""
        valid_explanations = [
            "Asere, esto está subiendo porque la economía está en candela. "
            "Con la inflación y el bloqueo (interno), el dólar se dispara como cohete.",
            "Mi socio, es por la escasez de fula. Cuando no hay billetes, "
            "todo el mundo quiere divisa y los precios se van pa'l cielo.",
            "Compadre, es la situación del país. Pocos dólares entrando "
            "y mucha gente necesitando. Así sube todo como la espuma.",
            "Oye hermano, con la crisis que hay, el que tiene dólares "
            "los vende caro. Es la ley de la oferta y la demanda asere.",
            "Mira, es simple: hay más demanda que oferta de divisa. "
            "Y cuando eso pasa en Cuba, los precios se van por la azotea.",
            "Asere, con la inflación galopante que tenemos, el peso cubano "
            "pierde valor cada día. Por eso las divisas suben como el pan.",
            "Hermano, es que no hay fula circulando. Y cuando escasea, "
            "el precio se va pa'rriba más rápido que bicicleta cuesta abajo.",
        ]

        result = get_random_exchange_explanation()

        assert result in valid_explanations

    def test_randomness(self):
        """Test that function can return different explanations."""
        results = {get_random_exchange_explanation() for _ in range(50)}

        # With 50 calls, we should get at least 3 different explanations
        assert len(results) >= 3
