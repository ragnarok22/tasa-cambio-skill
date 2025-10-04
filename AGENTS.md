# Repository Guidelines

## Project Structure & Module Organization
- `lambda/`: Alexa Lambda handlers (`lambda_function.py`) and helpers (`utils.py`); run-time deps pinned in `requirements.txt`.
- `skill-package/`: ASK manifest, locale-specific interaction models, and icon assets.
- Root files: `requirements-dev.txt` for tooling and `pyproject.toml` for Ruff configuration. No dedicated `tests/` directory yet—add one if you introduce automated coverage.

## Build, Test, and Development Commands
- Create environment: `cd lambda && python3 -m venv .venv && source .venv/bin/activate`.
- Install runtime deps: `pip install -r requirements.txt` (inside `lambda/`).
- Install dev tooling: `pip install -r requirements-dev.txt` (root).
- Lint & format: `ruff check lambda` and `ruff format lambda`.
- Package Lambda artifact:
  ```bash
  cd lambda
  rm -rf build && mkdir build
  pip install -r requirements.txt -t build/
  cp *.py build/
  cd build && zip -r ../lambda.zip .
  ```

## Coding Style & Naming Conventions
- Python 3.11+ with Ruff enforcing PEP 8-esque rules, 88-char lines, double quotes, and space indentation.
- Module names stay snake_case; handlers follow `*RequestHandler` pattern used in `lambda_function.py`.
- Keep responses in Cuban Spanish to match the skill’s persona.

## Testing Guidelines
- Preferred approach: exercise intents by importing `lambda.lambda_function.lambda_handler` with crafted Alexa payloads.
- When adding tests, place them under a new `tests/` package and name files `test_<feature>.py`; run with `pytest` (add to `requirements-dev.txt` as needed).
- Validate proxy integration by hitting `https://tasa-cambio-cuba.vercel.app/api/exchange-rate` or your local proxy before deployment.

## Commit & Pull Request Guidelines
- Follow existing history: conventional prefix (`docs:`, `chore(lint):`, `refactor(lambda):`) plus concise imperative summary.
- Reference tickets or issues in the body; describe user-facing Alexa changes and deployment steps.
- Include screenshots or transcript snippets when updating voice responses or interaction models.

## Security & Configuration Tips
- Do not hardcode credentials; rely on Lambda environment variables (`S3_PERSISTENCE_BUCKET`, `S3_PERSISTENCE_REGION`, proxy overrides).
- Rate data flows through the external proxy repo—verify its deployment status before releasing.
- Keep third-party dependencies minimal; remove unused libraries during packaging to control bundle size.
