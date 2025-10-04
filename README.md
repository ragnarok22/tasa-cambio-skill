# Tasa de Cambio Cubana

Alexa skill that answers in Cuban Spanish with up-to-date informal market exchange rates for USD, EUR, and MLC. The backend is an AWS Lambda written in Python and powered by the `ask-sdk`. Rates are retrieved through the companion proxy service [tasa-cambio-proxy](https://github.com/ragnarok22/tasa-cambio-proxy), which caches data from [El Toque](https://eltoque.com/tasas-de-cambio-de-moneda-en-cuba-hoy) and exposes a lightweight API hosted at [tasa-cambio-cuba.vercel.app](https://tasa-cambio-cuba.vercel.app/api/exchange-rate).

**Try it on Alexa:** [Tasa de Cambio Cubana on Amazon](https://www.amazon.com/dp/B0CLVSTJPB/)

## Key Features
- Launch prompt and conversational responses tailored to Cuban slang.
- `ExchangeRateIntent` for the full set of supported currencies.
- `ExchangeRateRequestIntent` slot (`CURRENCYTYPE`) to ask for a single currency such as "cuánto vale el dólar".
- Rates served via the proxy API to avoid hitting El Toque directly on every invocation.
- Fallback, help, and stop handlers already wired into the skill builder.

## Repository Layout
- `lambda/`: Alexa skill Lambda source, utilities, and runtime dependencies.
  - `lambda_function.py`: Main skill handlers and entry point.
  - `utils.py`: Helper functions for API calls and random greetings.
  - `requirements.txt`: Python dependencies (boto3 excluded as it's pre-installed).
  - `__init__.py`: Package marker for Python imports.
- `skill-package/`: ASK skill manifest, locale assets, and interaction models.
- `requirements-dev.txt`: Tooling for local linting (`ruff`).
- `pyproject.toml`: Formatting and lint configuration shared across the project.
- `ask-resources.json`: Alexa-hosted skill configuration.

## Data Source & Proxy
- Live API base: `https://tasa-cambio-cuba.vercel.app/api/exchange-rate`.
- Upstream rates scraped from El Toque and cached to minimize rate limits and latency.
- Proxy codebase: [ragnarok22/tasa-cambio-proxy](https://github.com/ragnarok22/tasa-cambio-proxy).
- When developing locally you can run the proxy project (Node.js) and point the Lambda to your local URL by overriding the constant in `lambda/utils.py`.

## Prerequisites
- Python 3.8+ (Alexa-hosted skills use Python 3.8 runtime).
- Alexa Skills Kit (ASK) CLI for deployment.
- Git access to the Alexa-hosted skill repository (configured automatically by ASK CLI).

## Local Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install runtime dependencies for the Lambda handler:
   ```bash
   pip install -r lambda/requirements.txt
   ```
3. (Optional) Install development tooling:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Run `ruff` to check formatting and linting:
   ```bash
   ruff check lambda/
   ruff format lambda/
   ```

## Local Testing Tips
- Create a simple invocation payload and call the handler directly:
  ```python
  from lambda.lambda_function import lambda_handler

  event = {"request": {"type": "LaunchRequest"}, "session": {"new": True}}
  lambda_handler(event, None)
  ```
- Use the [ASK Toolkit for VS Code](https://developer.amazon.com/en-US/alexa/alexa-skills-kit/get-deeper/tutorials-code-samples/hosted-skill-tutorial/local-debugging) or `ask smapi simulate` to converse with the skill once deployed.
- If you are running a local instance of the proxy, update the API base URL in `lambda/utils.py` or via an environment variable to target your local service.

## Deployment Workflow
This is an **Alexa-hosted skill**, which means AWS infrastructure is managed automatically. Deployment is done via Git:

1. Make your changes to the code in the `lambda/` directory
2. Commit your changes:
   ```bash
   git add .
   git commit -m "your changes"
   ```
3. Push to the master branch to deploy to development:
   ```bash
   git push origin master
   ```
4. AWS will automatically build and deploy your Lambda function
5. Monitor deployment status:
   ```bash
   ask smapi get-skill-status -s amzn1.ask.skill.af0ac2f5-8b03-40b9-a70a-e82372ffb852
   ```

**Note:** The `master` branch deploys to the development stage. The `prod` branch deploys to the live stage.

## Important Notes
- **Imports:** The Lambda uses absolute imports (`from utils import ...`) instead of relative imports to ensure compatibility with Alexa-hosted skill deployment.
- **Dependencies:** `boto3` is excluded from `requirements.txt` as it's pre-installed in AWS Lambda runtime.
- **Environment Variables:** The helper `create_presigned_url` expects `S3_PERSISTENCE_BUCKET` and `S3_PERSISTENCE_REGION` when used, but these are optional since the current handlers only call `get_exchange_rates`.

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
- [Tasa Cambio Proxy](https://github.com/ragnarok22/tasa-cambio-proxy)
