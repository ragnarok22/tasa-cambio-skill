# Repository Guidelines

## Project Structure & Module Organization
The Alexa runtime resides in `lambda/`, where `lambda_function.py` exposes the handler and `utils.py` centralizes helpers; runtime dependencies are pinned in `lambda/requirements.txt`. Voice models, icons, and the ASK manifest live in `skill-package/` under locale-specific subfolders. Repository-level tooling files (`pyproject.toml`, `requirements-dev.txt`) stay at the root. Introduce automated coverage inside a new top-level `tests/` package, mirroring module names for clarity.

## Build, Test, and Development Commands
- `cd lambda && python3 -m venv .venv && source .venv/bin/activate`: provision and activate the Lambda virtualenv.
- `pip install -r requirements.txt`: install production dependencies into the active venv.
- `pip install -r requirements-dev.txt`: add linting and testing tooling for local work.
- `ruff check lambda` / `ruff format lambda`: enforce linting and auto-format Python sources.
- Package for deployment with:
```bash
cd lambda
rm -rf build && mkdir build
pip install -r requirements.txt -t build/
cp *.py build/
cd build && zip -r ../lambda.zip .
```

## Coding Style & Naming Conventions
Target Python 3.11+, 4-space indentation, and double quotes for strings; Ruff enforces 88-character lines and general PEP 8 hygiene. Keep modules snake_case, class handlers following the `*RequestHandler` suffix, and ensure spoken responses remain in Cuban Spanish to match persona expectations.

## Testing Guidelines
Use `pytest` for intent and helper coverage; name files `tests/test_<feature>.py`. Craft Alexa request payloads and call `lambda.lambda_function.lambda_handler` directly to validate end-to-end behavior. Exercise proxy integrations against `https://tasa-cambio-cuba.vercel.app/api/exchange-rate` (or your staging proxy) before release.

## Commit & Pull Request Guidelines
Adopt conventional prefixes from history (`docs:`, `chore(lint):`, `refactor(lambda):`) followed by an imperative summary. Reference related tickets or issues in the body, describe user-visible Alexa changes, and include deployment notes. Attach interaction model diffs, transcripts, or screenshots whenever you adjust utterances or skill assets.

## Security & Configuration Tips
Never hardcode credentials; rely on Lambda environment variables such as `S3_PERSISTENCE_BUCKET` and `S3_PERSISTENCE_REGION`. Audit third-party libraries prior to packaging and prune unused ones to keep the artifact lean. Confirm the external exchange-rate proxy is reachable before shipping updates.
