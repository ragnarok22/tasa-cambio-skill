# -*- coding: utf-8 -*-

import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components.exception_components import (
    AbstractExceptionHandler,
)
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.response import Response
from utils import get_exchange_rates, get_random_greating

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = "Qué bola asere? Dime que quieres saber?"

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class ExchangeRateIntentHandler(AbstractRequestHandler):
    """Handler for Exchange Rates Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("ExchangeRateIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        """Return all exchange rates with dynamic USD/MLC comparison."""
        currencies = get_exchange_rates()

        mlc_value = round(currencies["MLC"], 2)
        usd_value = round(currencies["USD"], 2)
        eur_value = round(currencies["EUR"], 2)

        random_greating = get_random_greating()

        # Build dynamic comparison between USD and MLC
        usd_mlc_diff = abs(usd_value - mlc_value)
        if usd_mlc_diff < 5:
            usd_phrase = f"El U. S. D. casi en lo mismo, {usd_value} pesos"
        elif usd_value > mlc_value:
            usd_phrase = f"El U. S. D. un poco más arriba con {usd_value} pesos"
        else:
            usd_phrase = f"El U. S. D. en {usd_value} pesos"

        speak_output = (
            f"{random_greating}. El M. L. C. está en {mlc_value} pesos. "
            f"{usd_phrase}. Y el Euro ni se diga, ese anda por los {eur_value} pesos"
        )

        return handler_input.response_builder.speak(speak_output).response


class ExchangeRateRequestIntentHandler(AbstractRequestHandler):
    """Handler for Exchange Rates Request Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("ExchangeRateRequestIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        """Return exchange rate for a specific currency requested by the user."""
        currencies = get_exchange_rates()

        mlc_value = round(currencies["MLC"], 2)
        usd_value = round(currencies["USD"], 2)
        eur_value = round(currencies["EUR"], 2)

        slots = handler_input.request_envelope.request.intent.slots
        currency_type = slots["currency"].value

        logger.info(slots)

        if currency_type == "USD" or currency_type == "dólar":
            text_output = f"El U. S. D. anda por los {usd_value} pesos."
        elif currency_type == "euro":
            text_output = f"El Euro más caliente que el caribe. {eur_value} pesos."
        elif currency_type.upper() == "MLC":
            text_output = (
                f"El M. L. C. un poco por debajo del dólar a {mlc_value} pesos."
            )
        else:
            text_output = (
                f"Ni idea de lo que quieres decir compadre. "
                f"No conozco ningún {currency_type}"
            )

        random_greating = get_random_greating()
        speak_output = f"{random_greating}. {text_output}"

        return handler_input.response_builder.speak(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = (
            "Necesitas que te tire un cabo? Solo pregunta por las tasas de "
            "cambio de una moneda en específico y yo te tiro el dato asere."
        )

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = "Cuidate bro!"

        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = (
            "Hmm, No estoy seguro asere. Puedes decir Ayuda o preguntarme "
            "por cualquier moneda en Cuba. Dime que necesitas"
        )
        reprompt = "No entendí un carajo. En qué quieres que te tire un cabo?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.

    It will simply repeat the intent the user said. You can create custom
    handlers for your intents by defining them above, then also adding them
    to the request handler chain below.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return handler_input.response_builder.speak(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors.

    If you receive an error stating the request handler chain is not found,
    you have not implemented a handler for the intent being invoked or
    included it in the skill builder below.
    """

    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.error(exception, exc_info=True)

        speak_output = "Asere lo siento, tuve un problemilla ahí. Trata de nuevo."

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


# Skill builder configuration
# Handler order matters - they're processed top to bottom
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExchangeRateIntentHandler())
sb.add_request_handler(ExchangeRateRequestIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# IntentReflectorHandler must be last to avoid overriding custom handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
