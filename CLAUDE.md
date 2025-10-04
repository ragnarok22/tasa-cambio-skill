# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alexa Skill for providing Cuban exchange rates (USD, EUR, MLC) in the informal market. The skill uses colloquial Cuban Spanish phrases and fetches data from `https://tasa-cambio-cuba.vercel.app/api/exchange-rate`.

## Architecture

**Deployment Type:** Alexa-hosted skill (AWS infrastructure managed automatically via Git push)

**Lambda Function Structure:**
- `lambda/lambda_function.py`: Main entry point with ASK SDK request handlers
  - Uses **absolute imports** (`import utils` / `from utils import ...`) for Alexa-hosted compatibility
  - Handlers follow ASK SDK pattern: `can_handle()` + `handle()` methods
  - Entry point: `lambda_handler = sb.lambda_handler()`

- `lambda/utils.py`: Utility functions
  - `get_exchange_rates()`: Fetches current rates from API via requests (with timeout and error handling)
  - `get_rounded_exchange_rates()`: Helper that fetches and rounds rates to 2 decimals
  - `get_random_greeting()`: Returns random Cuban greeting phrases
  - `create_presigned_url()`: S3 utility (currently unused)

- `lambda/__init__.py`: Empty file required for Python package recognition

- `lambda/requirements.txt`: Production dependencies
  - **Does NOT include boto3** (pre-installed in Lambda runtime)
  - Uses flexible version ranges to avoid build failures (e.g., `requests>=2.31.0,<3.0.0`)

**Skill Package Structure:**
- `skill-package/skill.json`: Alexa skill manifest with endpoint ARNs for NA, EU, FE regions
- `skill-package/interactionModels/custom/`: Interaction models for es-US, es-MX, es-ES locales
  - Invocation name: "tarifa cambio"
  - Main intents: `ExchangeRateIntent` (all rates), `ExchangeRateRequestIntent` (specific currency)
  - Custom slot type: `CURRENCYTYPE` with values USD, MLC, euro

**Build Environment:** Python 3.8 runtime (Alexa-hosted skills constraint)

## Development Commands

**Dependencies:**
```bash
# Install production dependencies
pip install -r lambda/requirements.txt

# Install dev dependencies (ruff, pytest, coverage)
pip install -r requirements-dev.txt
```

**Code Quality:**
```bash
# Format code
ruff format lambda/

# Lint code
ruff check lambda/
```

**Testing:**
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=lambda --cov-report=term-missing

# Run specific test file
pytest tests/test_utils.py -v

# Compile Python files (syntax check)
python3 -m py_compile lambda/*.py
```

Current test coverage: **84%** (25 tests)

**Deployment:**
This is an Alexa-hosted skill. Deployment happens automatically via Git:
```bash
# Push to master for development deployment
git push origin master

# Monitor deployment status
ask smapi get-skill-status -s amzn1.ask.skill.af0ac2f5-8b03-40b9-a70a-e82372ffb852
```

**Debugging Failed Deployments:**
Build logs are in CloudWatch under log group `/aws/codebuild/Build-af0ac2f5-...`
Common failures:
- Dependency version not available in build environment (use flexible version ranges)
- Missing `__init__.py` (required for package imports)
- Using relative imports instead of absolute imports

## Important Notes

- The lambda function uses **absolute imports** (`from utils import ...`) for Alexa-hosted skill compatibility
- `boto3` must NOT be in `requirements.txt` (pre-installed in Lambda, causes build failures if pinned to unavailable versions)
- All Spanish responses use Cuban slang ("asere", "en talla", "qué bolá", etc.)
- The skill supports 3 Spanish locales: es-US, es-MX, es-ES
- Exchange rate API endpoint: `https://tasa-cambio-cuba.vercel.app/api/exchange-rate`
- Returns JSON with keys: `usd`, `eur`, `mlc`
- Git master branch → development stage, prod branch → live stage
