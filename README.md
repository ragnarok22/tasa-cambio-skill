# Tasa de Cambio Cubana

Alexa skill that answers in Cuban Spanish with up-to-date informal market exchange rates for USD, EUR, and MLC. The backend is an AWS Lambda written in Python and powered by the `ask-sdk`. Rates are retrieved from [tasa-cambio-cuba.vercel.app](https://tasa-cambio-cuba.vercel.app/api/exchange-rate), which mirrors the data published by [eltoque.com](https://eltoque.com/tasas-de-cambio-de-moneda-en-cuba-hoy).

## Key Features
- Launch prompt and conversational responses tailored to Cuban slang.
- `ExchangeRateIntent` for the full set of supported currencies.
- `ExchangeRateRequestIntent` slot (`CURRENCYTYPE`) to ask for a single currency such as "cuánto vale el dólar".
- Fallback, help, and stop handlers already wired into the skill builder.

## Repository Layout
- `lambda/`: Alexa skill Lambda source, utilities, and runtime dependencies.
- `skill-package/`: ASK skill manifest, locale assets, and interaction models.
- `requirements-dev.txt`: Tooling for local linting (`ruff`).
- `pyproject.toml`: Formatting and lint configuration shared across the project.

## Prerequisites
- Python 3.11+ (project targets Python 3.13 but 3.11 works well for AWS Lambda today).
- AWS CLI configured with credentials that can update the target Lambda function.
- Alexa Skills Kit (ASK) CLI if you plan to update the skill package.

## Local Setup
1. Create and activate a virtual environment:
   ```bash
   cd lambda
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install runtime dependencies for the Lambda handler:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Install development tooling at the repository root:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Run `ruff` to check formatting and linting:
   ```bash
   ruff check lambda
   ruff format lambda
   ```

## Local Testing Tips
- Create a simple invocation payload and call the handler directly:
  ```python
  from lambda.lambda_function import lambda_handler

  event = {"request": {"type": "LaunchRequest"}, "session": {"new": True}}
  lambda_handler(event, None)
  ```
- Use the [ASK Toolkit for VS Code](https://developer.amazon.com/en-US/alexa/alexa-skills-kit/get-deeper/tutorials-code-samples/hosted-skill-tutorial/local-debugging) or `ask smapi simulate` to converse with the skill once deployed.

## Deployment Workflow
1. Export the Lambda payload with dependencies:
   ```bash
   cd lambda
   rm -rf build && mkdir build
   pip install -r requirements.txt -t build/
   cp *.py build/
   cd build && zip -r ../lambda.zip .
   ```
2. Update the AWS Lambda function:
   ```bash
   aws lambda update-function-code \
     --function-name <lambda-function-name> \
     --zip-file fileb://lambda.zip
   ```
3. Deploy the Alexa skill resources (requires `ask cli` configuration):
   ```bash
   ask deploy --target skill
   ```

## Environment Variables
The helper `create_presigned_url` expects the following variables when used:
- `S3_PERSISTENCE_BUCKET`
- `S3_PERSISTENCE_REGION`

They are optional today because the Lambda handlers only call `get_exchange_rates`, but the function is ready for future use cases that need short-lived links to S3 assets.

## Skill Configuration Notes
- Invocation name: `tarifa cambio`.
- Supported locales: `es-US`, `es-ES`, `es-MX` (with shared interaction model and localized icons).
- Custom slot `CURRENCYTYPE` with values for USD, MLC, and EUR plus Cuban Spanish synonyms.

## Contributing
1. Fork and branch from `main`.
2. Keep responses in Cuban Spanish to maintain voice consistency.
3. Run `ruff check` before pushing changes.
4. Open a pull request describing user-facing changes and deployment considerations.

## Useful Links
- [Alexa Skills Kit documentation](https://developer.amazon.com/en-US/docs/alexa/ask-overviews/what-is-the-alexa-skills-kit.html)
- [ASK CLI reference](https://developer.amazon.com/en-US/docs/alexa/smapi/smapi-cli-reference.html)
- [AWS Lambda Python packaging](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
