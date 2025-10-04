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
  - Handler registration order matters (processed top to bottom in skill builder)

- `lambda/utils.py`: Utility functions
  - `get_exchange_rates()`: Fetches current rates from API via requests (with timeout and error handling)
  - `get_rounded_exchange_rates()`: Helper that fetches and rounds rates to 2 decimals
  - `get_random_greeting()`: Returns random Cuban greeting phrases
  - `get_random_exchange_explanation()`: Returns random Cuban explanations for why rates are rising
  - `create_presigned_url()`: S3 utility (currently unused)

- `lambda/__init__.py`: Empty file required for Python package recognition

- `lambda/requirements.txt`: Production dependencies
  - **Does NOT include boto3** (pre-installed in Lambda runtime)
  - Uses flexible version ranges to avoid build failures (e.g., `requests>=2.31.0,<3.0.0`)

**Skill Package Structure:**
- `skill-package/skill.json`: Alexa skill manifest with endpoint ARNs for NA, EU, FE regions
- `skill-package/interactionModels/custom/`: Interaction models for es-US, es-MX, es-ES locales
  - Invocation name: "tarifa cambio"
  - Main intents:
    - `ExchangeRateIntent`: Returns all currency rates
    - `ExchangeRateRequestIntent`: Returns specific currency rate (with CURRENCYTYPE slot)
    - `ConvertCurrencyIntent`: Converts foreign currency to Cuban pesos (with amount and sourceCurrency slots)
    - `WhyExchangeRateIntent`: Explains why exchange rates are rising with Cuban slang
  - Custom slot type: `CURRENCYTYPE` with values USD, MLC, euro

**Build Environment:** Python 3.8 runtime (Alexa-hosted skills constraint, but tests run on Python 3.9+)

## Development Commands

**Using Makefile (recommended):**
```bash
make help          # Show all available commands
make install       # Install production dependencies
make install-dev   # Install dev dependencies (ruff, pytest, coverage)
make format        # Format code with ruff
make check         # Check code formatting without changes
make lint          # Lint code with ruff
make lint-fix      # Lint and auto-fix issues
make test          # Run tests
make coverage      # Run tests with coverage report
make coverage-html # Generate HTML coverage report
make compile       # Compile Python files (syntax check)
make all           # Run format, lint, and test
make ci            # Run CI checks (format check, lint, coverage)
make clean         # Clean up generated files
```

**Direct commands (if not using make):**
```bash
# Dependencies
pip install -r lambda/requirements.txt      # Production
pip install -r requirements-dev.txt         # Development

# Code quality
ruff format lambda/                         # Format
ruff check lambda/                          # Lint

# Testing (requires venv activation)
source .venv/bin/activate
pytest                                      # Run all tests
pytest --cov=lambda --cov-report=term-missing  # With coverage
pytest tests/test_utils.py -v               # Specific test file
```

Current test coverage: **84%+** (28+ tests covering utils and all handlers)

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

**Critical Deployment Constraints:**
- The lambda function uses **absolute imports** (`from utils import ...`) for Alexa-hosted skill compatibility - never use relative imports
- `boto3` must NOT be in `requirements.txt` (pre-installed in Lambda, causes build failures if pinned to unavailable versions)
- Use flexible version ranges in requirements.txt (e.g., `requests>=2.31.0,<3.0.0`) to avoid build failures
- `lambda/__init__.py` must exist (even if empty) for package imports to work

**Cuban Spanish Voice:**
- All Spanish responses use Cuban slang ("asere", "en talla", "qué bolá", "fula", "pa'rriba", etc.)
- When adding new responses, maintain authentic Cuban voice consistency
- Random greeting and explanation functions provide variety while keeping the Cuban character

**Interaction Model:**
- All three locale files (es-US, es-MX, es-ES) must be kept in sync
- When adding new intents, update all three interaction model files
- The skill supports 3 Spanish locales but uses the same Cuban slang across all

**API Integration:**
- Exchange rate API endpoint: `https://tasa-cambio-cuba.vercel.app/api/exchange-rate`
- Returns JSON with keys: `usd`, `eur`, `mlc`
- 5-second timeout configured in `get_exchange_rates()`

**Git Workflow:**
- Git master branch → development stage
- Git prod branch → live stage
- Deployment is automatic via Git push
