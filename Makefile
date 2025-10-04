.PHONY: help install install-dev format check lint test coverage clean compile all

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r lambda/requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

format:  ## Format code with ruff
	ruff format lambda/

check:  ## Check code formatting without making changes
	ruff format --check lambda/

lint:  ## Lint code with ruff
	ruff check lambda/

lint-fix:  ## Lint and auto-fix issues with ruff
	ruff check --fix lambda/

test:  ## Run tests with pytest
	pytest

coverage:  ## Run tests with coverage report
	pytest --cov=lambda --cov-report=term-missing

coverage-html:  ## Generate HTML coverage report
	pytest --cov=lambda --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

compile:  ## Compile Python files to check for syntax errors
	python3 -m py_compile lambda/*.py

all: format lint test  ## Run format, lint, and test

ci: check lint coverage  ## Run CI checks (format check, lint, coverage)

clean:  ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf lambda/__pycache__
	rm -rf tests/__pycache__
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
