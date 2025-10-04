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
from utils import (
    get_random_exchange_explanation,
    get_random_greeting,
    get_rounded_exchange_rates,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("Processing LaunchRequest")
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
        logger.info("Processing ExchangeRateIntent")
        currencies = get_rounded_exchange_rates()

        if currencies is None:
            logger.warning("Failed to fetch exchange rates")
            speak_output = (
                "Coño asere, tengo un problema conectándome. "
                "Intenta de nuevo en un ratito."
            )
            return handler_input.response_builder.speak(speak_output).response

        mlc_value = currencies["MLC"]
        usd_value = currencies["USD"]
        eur_value = currencies["EUR"]

        logger.info(f"Rates: USD={usd_value}, EUR={eur_value}, MLC={mlc_value}")
        random_greeting = get_random_greeting()

        # Build dynamic comparison between USD and MLC
        usd_mlc_diff = abs(usd_value - mlc_value)
        if usd_mlc_diff < 5:
            usd_phrase = f"El U. S. D. casi en lo mismo, {usd_value} pesos"
        elif usd_value > mlc_value:
            usd_phrase = f"El U. S. D. un poco más arriba con {usd_value} pesos"
        else:
            usd_phrase = f"El U. S. D. en {usd_value} pesos"

        speak_output = (
            f"{random_greeting}. El M. L. C. está en {mlc_value} pesos. "
            f"{usd_phrase}. Y el Euro ni se diga, ese anda por los {eur_value} pesos"
        )

        return handler_input.response_builder.speak(speak_output).response


class ExchangeRateRequestIntentHandler(AbstractRequestHandler):
    """Handler for Exchange Rates Request Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("ExchangeRateRequestIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        """Return exchange rate for a specific currency requested by the user."""
        logger.info("Processing ExchangeRateRequestIntent")
        currencies = get_rounded_exchange_rates()

        if currencies is None:
            logger.warning("Failed to fetch exchange rates")
            speak_output = (
                "Coño asere, tengo un problema conectándome. "
                "Intenta de nuevo en un ratito."
            )
            return handler_input.response_builder.speak(speak_output).response

        mlc_value = currencies["MLC"]
        usd_value = currencies["USD"]
        eur_value = currencies["EUR"]

        slots = handler_input.request_envelope.request.intent.slots
        currency_slot = slots.get("currency")

        if not currency_slot or not currency_slot.value:
            logger.warning("Currency slot is empty or missing")
            speak_output = (
                "No te entendí bien asere. Dime qué moneda quieres saber: "
                "dólar, euro o M. L. C."
            )
            return handler_input.response_builder.speak(speak_output).response

        currency_type = currency_slot.value
        logger.info(f"Requested currency: {currency_type}")

        if currency_type == "USD" or currency_type == "dólar":
            text_output = f"El U. S. D. anda por los {usd_value} pesos."
        elif currency_type == "euro":
            text_output = f"El Euro más caliente que el caribe. {eur_value} pesos."
        elif currency_type.upper() == "MLC":
            mlc_usd_diff = abs(mlc_value - usd_value)
            if mlc_usd_diff < 5:
                text_output = f"El M. L. C. casi igual que el dólar, {mlc_value} pesos."
            elif mlc_value < usd_value:
                text_output = (
                    f"El M. L. C. un poco por debajo del dólar a {mlc_value} pesos."
                )
            else:
                text_output = f"El M. L. C. está en {mlc_value} pesos."
        else:
            text_output = (
                f"Ni idea de lo que quieres decir compadre. "
                f"No conozco ningún {currency_type}"
            )

        random_greeting = get_random_greeting()
        speak_output = f"{random_greeting}. {text_output}"

        return handler_input.response_builder.speak(speak_output).response


class ConvertCurrencyIntentHandler(AbstractRequestHandler):
    """Handler for Currency Conversion Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("ConvertCurrencyIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        """Convert amount from foreign currency to Cuban pesos."""
        logger.info("Processing ConvertCurrencyIntent")
        currencies = get_rounded_exchange_rates()

        if currencies is None:
            logger.warning("Failed to fetch exchange rates")
            speak_output = (
                "Coño asere, tengo un problema conectándome. "
                "Intenta de nuevo en un ratito."
            )
            return handler_input.response_builder.speak(speak_output).response

        slots = handler_input.request_envelope.request.intent.slots
        amount_slot = slots.get("amount")
        currency_slot = slots.get("sourceCurrency")

        if not amount_slot or not amount_slot.value:
            logger.warning("Amount slot is empty or missing")
            speak_output = (
                "No te entendí bien asere. Dime la cantidad que quieres convertir."
            )
            return handler_input.response_builder.speak(speak_output).response

        if not currency_slot or not currency_slot.value:
            logger.warning("Currency slot is empty or missing")
            speak_output = "No te entendí la moneda asere. Dime dólar, euro o M. L. C."
            return handler_input.response_builder.speak(speak_output).response

        try:
            amount = float(amount_slot.value)
        except ValueError:
            logger.warning(f"Invalid amount value: {amount_slot.value}")
            speak_output = "No entendí la cantidad asere. Dime un número."
            return handler_input.response_builder.speak(speak_output).response

        currency_type = currency_slot.value
        logger.info(f"Converting {amount} {currency_type} to CUP")

        # Get exchange rate
        rate = None
        currency_name = ""
        if currency_type == "USD" or currency_type == "dólar":
            rate = currencies["USD"]
            currency_name = "dólares"
        elif currency_type == "euro":
            rate = currencies["EUR"]
            currency_name = "euros"
        elif currency_type.upper() == "MLC":
            rate = currencies["MLC"]
            currency_name = "M. L. C."
        else:
            speak_output = (
                f"Ni idea de lo que quieres decir compadre. "
                f"No conozco ningún {currency_type}"
            )
            return handler_input.response_builder.speak(speak_output).response

        # Calculate conversion
        total_pesos = round(amount * rate, 2)

        # Format output
        amount_str = str(int(amount)) if amount == int(amount) else str(amount)
        total_str = (
            str(int(total_pesos))
            if total_pesos == int(total_pesos)
            else str(total_pesos)
        )

        random_greeting = get_random_greeting()
        speak_output = (
            f"{random_greeting}. {amount_str} {currency_name} "
            f"son {total_str} pesos cubanos."
        )

        return handler_input.response_builder.speak(speak_output).response


class WhyExchangeRateIntentHandler(AbstractRequestHandler):
    """Handler for Why Exchange Rate Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("WhyExchangeRateIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        """Return a random Cuban explanation for currency increase."""
        logger.info("Processing WhyExchangeRateIntent")
        speak_output = get_random_exchange_explanation()

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
        logger.error(f"Unhandled exception: {exception}", exc_info=True)

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
sb.add_request_handler(ConvertCurrencyIntentHandler())
sb.add_request_handler(WhyExchangeRateIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# IntentReflectorHandler must be last to avoid overriding custom handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
