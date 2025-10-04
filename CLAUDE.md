# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alexa Skill for providing Cuban exchange rates (USD, EUR, MLC) in the informal market. The skill uses colloquial Cuban Spanish phrases and fetches data from `https://tasa-cambio-cuba.vercel.app/api/exchange-rate`.

## Architecture

**Lambda Function Structure:**
- `lambda/lambda_function.py`: Main entry point with ASK SDK request handlers
  - Uses relative import `from .utils import ...` (required for AWS Lambda deployment)
  - Handlers follow ASK SDK pattern: `can_handle()` + `handle()` methods
  - Entry point: `lambda_handler = sb.lambda_handler()`

- `lambda/utils.py`: Utility functions
  - `get_exchange_rates()`: Fetches current rates from API
  - `get_random_greating()`: Returns random Cuban greeting phrases
  - `create_presigned_url()`: S3 utility (currently unused)

**Skill Package Structure:**
- `skill-package/skill.json`: Alexa skill manifest with endpoint ARNs for NA, EU, FE regions
- `skill-package/interactionModels/custom/`: Interaction models for es-US, es-MX, es-ES locales
  - Invocation name: "tarifa cambio"
  - Main intents: `ExchangeRateIntent` (all rates), `ExchangeRateRequestIntent` (specific currency)
  - Custom slot type: `CURRENCYTYPE` with values USD, MLC, euro

## Development Commands

**Dependencies:**
```bash
# Install production dependencies
pip install -r lambda/requirements.txt

# Install dev dependencies (ruff)
pip install -r requirements-dev.txt
```

**Code Quality:**
```bash
# Format code
ruff format lambda/

# Lint code
ruff check lambda/
```

**Testing Compilation:**
```bash
# Compile Python files (syntax check)
python -m py_compile lambda/*.py

# Note: Relative imports in lambda_function.py will fail when imported directly
# This is expected - the code is designed for AWS Lambda execution context
```

**Deployment:**
This is an AWS-hosted Alexa skill. Use ASK CLI for deployment:
```bash
ask deploy
```

## Important Notes

- The lambda function uses **relative imports** (`from .utils import ...`) which is the correct pattern for AWS Lambda but will fail in local Python imports
- All Spanish responses use Cuban slang ("asere", "en talla", "qué bolá", etc.)
- The skill supports 3 Spanish locales: es-US, es-MX, es-ES
- Exchange rate API endpoint: `https://tasa-cambio-cuba.vercel.app/api/exchange-rate`
- Returns JSON with keys: `usd`, `eur`, `mlc`
