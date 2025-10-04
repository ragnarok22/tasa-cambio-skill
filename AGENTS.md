# Repository Guidelines

## Project Structure & Module Organization
- Core Alexa runtime lives in `lambda/` with `lambda_function.py` exposing the handler and shared helpers in `utils.py`.
- Production dependencies pin in `lambda/requirements.txt`; voice models and assets reside in `skill-package/` under locale folders.
- Place automated tests inside `tests/`, mirroring module names (e.g., `tests/test_utils.py`) for fast discovery.

## Build, Test, and Development Commands
- `cd lambda && python3 -m venv .venv && source .venv/bin/activate`: create and activate the Lambda virtualenv.
- `pip install -r requirements.txt` followed by `pip install -r ../requirements-dev.txt`: install runtime then dev tooling inside the venv.
- `ruff check lambda` and `ruff format lambda`: lint and auto-format Python sources.
- Packaging: 
  ```bash
  cd lambda
  rm -rf build && mkdir build
  pip install -r requirements.txt -t build/
  cp *.py build/
  cd build && zip -r ../lambda.zip .
  ```

## Coding Style & Naming Conventions
- Target Python 3.11+, 4-space indentation, and double-quoted strings; Ruff enforces 88-character lines and PEP 8.
- Keep module filenames snake_case; Alexa handlers end with `*RequestHandler` and spoken responses stay in Cuban Spanish.

## Testing Guidelines
- Use `pytest` from the repository root or inside `lambda/` once the venv is active.
- Name test modules `tests/test_<feature>.py` and drive end-to-end checks by calling `lambda.lambda_function.lambda_handler` with Alexa request payloads.
- Aim for meaningful coverage of both helper functions and request handlers as new features land.

## Commit & Pull Request Guidelines
- Follow the existing conventional prefixes such as `docs:`, `chore(lint):`, or `refactor(lambda):` with an imperative description.
- Reference related tickets, describe user-visible Alexa impacts, and add deployment notes in the commit or PR body.
- Attach interaction model diffs, transcripts, or screenshots whenever changing utterances or skill assets.

## Security & Configuration Tips
- Never hardcode credentials; rely on environment variables like `S3_PERSISTENCE_BUCKET` and `S3_PERSISTENCE_REGION`.
- Audit third-party libraries before packaging and prune unused dependencies to keep the Lambda artifact lean.
- Confirm `https://tasa-cambio-cuba.vercel.app/api/exchange-rate` (or the staging proxy) is reachable before publishing updates.
