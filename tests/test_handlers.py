"""Tests for Alexa skill handlers."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add lambda directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lambda"))

from lambda_function import (
    CancelOrStopIntentHandler,
    CatchAllExceptionHandler,
    ExchangeRateIntentHandler,
    ExchangeRateRequestIntentHandler,
    FallbackIntentHandler,
    HelpIntentHandler,
    LaunchRequestHandler,
)


class TestLaunchRequestHandler:
    """Tests for LaunchRequestHandler."""

    def test_can_handle_launch_request(self):
        """Test handler can handle LaunchRequest."""
        handler = LaunchRequestHandler()
        handler_input = Mock()
        handler_input.request_envelope.request.request_type = "LaunchRequest"

        with patch("lambda_function.ask_utils.is_request_type") as mock_is_type:
            mock_is_type.return_value = lambda x: True
            result = handler.can_handle(handler_input)

        assert result is True

    def test_handle_returns_welcome_message(self):
        """Test handler returns correct welcome message."""
        handler = LaunchRequestHandler()
        handler_input = Mock()
        response_builder = Mock()
        handler_input.response_builder = response_builder

        handler.handle(handler_input)

        response_builder.speak.assert_called_once_with(
            "Qué bola asere? Dime que quieres saber?"
        )


class TestExchangeRateIntentHandler:
    """Tests for ExchangeRateIntentHandler."""

    @patch("lambda_function.get_rounded_exchange_rates")
    @patch("lambda_function.get_random_greeting")
    def test_successful_response_with_close_values(
        self, mock_greeting, mock_get_rates
    ):
        """Test successful response when USD and MLC are close."""
        handler = ExchangeRateIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = {"USD": 120.0, "EUR": 130.0, "MLC": 118.0}
        mock_greeting.return_value = "En talla asere"

        result = handler.handle(handler_input)

        assert "El M. L. C. está en 118.0 pesos" in str(
            handler_input.response_builder.speak.call_args
        )
        assert "El U. S. D. casi en lo mismo, 120.0 pesos" in str(
            handler_input.response_builder.speak.call_args
        )

    @patch("lambda_function.get_rounded_exchange_rates")
    @patch("lambda_function.get_random_greeting")
    def test_successful_response_usd_higher(self, mock_greeting, mock_get_rates):
        """Test response when USD is higher than MLC."""
        handler = ExchangeRateIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = {"USD": 125.0, "EUR": 130.0, "MLC": 115.0}
        mock_greeting.return_value = "En talla asere"

        handler.handle(handler_input)

        assert "El U. S. D. un poco más arriba con 125.0 pesos" in str(
            handler_input.response_builder.speak.call_args
        )

    @patch("lambda_function.get_rounded_exchange_rates")
    def test_api_failure(self, mock_get_rates):
        """Test handler when API fails."""
        handler = ExchangeRateIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = None

        handler.handle(handler_input)

        assert "Coño asere, tengo un problema conectándome" in str(
            handler_input.response_builder.speak.call_args
        )


class TestExchangeRateRequestIntentHandler:
    """Tests for ExchangeRateRequestIntentHandler."""

    @patch("lambda_function.get_rounded_exchange_rates")
    @patch("lambda_function.get_random_greeting")
    def test_request_usd(self, mock_greeting, mock_get_rates):
        """Test requesting USD rate."""
        handler = ExchangeRateRequestIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = {"USD": 120.0, "EUR": 130.0, "MLC": 118.0}
        mock_greeting.return_value = "En talla asere"

        # Mock slots
        currency_slot = Mock()
        currency_slot.value = "USD"
        handler_input.request_envelope.request.intent.slots = {"currency": currency_slot}

        handler.handle(handler_input)

        assert "El U. S. D. anda por los 120.0 pesos" in str(
            handler_input.response_builder.speak.call_args
        )

    @patch("lambda_function.get_rounded_exchange_rates")
    @patch("lambda_function.get_random_greeting")
    def test_request_mlc_below_usd(self, mock_greeting, mock_get_rates):
        """Test requesting MLC when it's below USD."""
        handler = ExchangeRateRequestIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = {"USD": 125.0, "EUR": 130.0, "MLC": 115.0}
        mock_greeting.return_value = "En talla asere"

        currency_slot = Mock()
        currency_slot.value = "MLC"
        handler_input.request_envelope.request.intent.slots = {"currency": currency_slot}

        handler.handle(handler_input)

        assert "El M. L. C. un poco por debajo del dólar a 115.0 pesos" in str(
            handler_input.response_builder.speak.call_args
        )

    @patch("lambda_function.get_rounded_exchange_rates")
    def test_missing_slot(self, mock_get_rates):
        """Test handler when slot is missing."""
        handler = ExchangeRateRequestIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = {"USD": 120.0, "EUR": 130.0, "MLC": 118.0}

        handler_input.request_envelope.request.intent.slots = {}

        handler.handle(handler_input)

        assert "No te entendí bien asere" in str(
            handler_input.response_builder.speak.call_args
        )

    @patch("lambda_function.get_rounded_exchange_rates")
    def test_unknown_currency(self, mock_get_rates):
        """Test handler with unknown currency."""
        handler = ExchangeRateRequestIntentHandler()
        handler_input = Mock()
        mock_get_rates.return_value = {"USD": 120.0, "EUR": 130.0, "MLC": 118.0}

        currency_slot = Mock()
        currency_slot.value = "bitcoin"
        handler_input.request_envelope.request.intent.slots = {"currency": currency_slot}

        handler.handle(handler_input)

        assert "Ni idea de lo que quieres decir compadre" in str(
            handler_input.response_builder.speak.call_args
        )


class TestHelpIntentHandler:
    """Tests for HelpIntentHandler."""

    def test_handle_returns_help_message(self):
        """Test handler returns help message."""
        handler = HelpIntentHandler()
        handler_input = Mock()

        handler.handle(handler_input)

        assert "Necesitas que te tire un cabo" in str(
            handler_input.response_builder.speak.call_args
        )


class TestCancelOrStopIntentHandler:
    """Tests for CancelOrStopIntentHandler."""

    def test_handle_returns_goodbye(self):
        """Test handler returns goodbye message."""
        handler = CancelOrStopIntentHandler()
        handler_input = Mock()

        handler.handle(handler_input)

        assert "Cuidate bro" in str(handler_input.response_builder.speak.call_args)


class TestFallbackIntentHandler:
    """Tests for FallbackIntentHandler."""

    def test_handle_returns_fallback_message(self):
        """Test handler returns fallback message."""
        handler = FallbackIntentHandler()
        handler_input = Mock()

        handler.handle(handler_input)

        assert "No estoy seguro asere" in str(
            handler_input.response_builder.speak.call_args
        )


class TestCatchAllExceptionHandler:
    """Tests for CatchAllExceptionHandler."""

    def test_can_handle_any_exception(self):
        """Test handler can handle any exception."""
        handler = CatchAllExceptionHandler()
        handler_input = Mock()
        exception = Exception("Test error")

        result = handler.can_handle(handler_input, exception)

        assert result is True

    def test_handle_logs_and_returns_error_message(self):
        """Test handler logs exception and returns error message."""
        handler = CatchAllExceptionHandler()
        handler_input = Mock()
        exception = Exception("Test error")

        handler.handle(handler_input, exception)

        assert "Asere lo siento, tuve un problemilla ahí" in str(
            handler_input.response_builder.speak.call_args
        )
