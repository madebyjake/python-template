# Package configuration
PACKAGE_NAME ?= python-template
SCRIPT_NAME ?= python-template
MAIN_MODULE ?= main
MAIN_FUNCTION ?= main

# Version extraction command (uses built-in tomllib for Python 3.11+)
GET_VERSION = uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

.PHONY: help install install-dev test test-cov run debug run-pkg debug-pkg lint format type-check clean build publish docs serve-docs version bump bump-major bump-minor bump-patch lock sync add remove tree

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

install-dev: ## Install all dependencies including dev
	uv sync --extra dev

lock: ## Lock dependencies
	uv lock

sync: ## Sync dependencies with lockfile
	uv sync

add: ## Add a dependency (usage: make add PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Error: PACKAGE is required. Usage: make add PACKAGE=package-name"; \
		exit 1; \
	fi
	uv add $(PACKAGE)

remove: ## Remove a dependency (usage: make remove PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Error: PACKAGE is required. Usage: make remove PACKAGE=package-name"; \
		exit 1; \
	fi
	uv remove $(PACKAGE)

tree: ## Show dependency tree
	uv tree

setup: ## Complete development setup
	@echo "Setting up development environment..."
	@uv sync --extra dev || (echo "Error: Failed to install dependencies" && exit 1)
	@uv run pre-commit install || (echo "Error: Failed to install pre-commit hooks" && exit 1)
	@echo "Development environment ready!"

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

run: ## Run the application (usage: make run [package] [ARGS="--help"])
	@if [ -n "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		uv run python -c "from $(filter-out $@,$(MAKECMDGOALS)).$(MAIN_MODULE) import $(MAIN_FUNCTION); $(MAIN_FUNCTION)()" $(ARGS) || (echo "Error: Failed to run application" && exit 1); \
	else \
		uv run $(SCRIPT_NAME) $(ARGS) || (echo "Error: Failed to run $(SCRIPT_NAME)" && exit 1); \
	fi

debug: ## Run in debug mode (usage: make debug [package] [ARGS="--help"])
	@if [ -n "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		uv run python -c "from $(filter-out $@,$(MAKECMDGOALS)).$(MAIN_MODULE) import $(MAIN_FUNCTION); $(MAIN_FUNCTION)()" $(ARGS) || (echo "Error: Failed to run application in debug mode" && exit 1); \
	else \
		uv run python -c "from src.cli.$(MAIN_MODULE) import $(MAIN_FUNCTION); $(MAIN_FUNCTION)()" $(ARGS) || (echo "Error: Failed to run $(SCRIPT_NAME) in debug mode" && exit 1); \
	fi

%:
	@:

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .

type-check: ## Run type checking
	uv run mypy src/

check: lint type-check test ## Run all checks

check-fast: lint ## Run fast checks (lint only)
	@echo "Running fast checks..."

check-full: lint type-check test test-cov ## Run all checks including coverage
	@echo "Running full checks with coverage..."

format-check: ## Check if code is formatted correctly
	uv run ruff format --check .

format-fix: ## Format code and fix issues
	uv run ruff format .
	uv run ruff check --fix .

benchmark: ## Benchmark linting and formatting performance
	@echo "Benchmarking Ruff performance..."
	@time uv run ruff check .
	@echo "Benchmarking Ruff formatting..."
	@time uv run ruff format --check .

profile: ## Profile dependency resolution
	@echo "Profiling UV dependency resolution..."
	uv lock --verbose

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## Build the package
	@if [ ! -f pyproject.toml ]; then \
		echo "Error: pyproject.toml not found" && exit 1; \
	fi
	uv build || (echo "Error: Failed to build package" && exit 1)

publish: ## Publish to PyPI
	@if [ ! -d dist ]; then \
		echo "Error: No dist directory found. Run 'make build' first." && exit 1; \
	fi
	uv publish || (echo "Error: Failed to publish to PyPI" && exit 1)

docs: ## Build documentation
	@if [ ! -f mkdocs.yml ]; then \
		echo "Error: mkdocs.yml not found. MkDocs may have been removed." && exit 1; \
	fi
	uv run mkdocs build || (echo "Error: Failed to build documentation" && exit 1)

serve-docs: ## Serve documentation locally
	@if [ ! -f mkdocs.yml ]; then \
		echo "Error: mkdocs.yml not found. MkDocs may have been removed." && exit 1; \
	fi
	uv run mkdocs serve || (echo "Error: Failed to serve documentation" && exit 1)

version: ## Show current version
	@if [ ! -f pyproject.toml ]; then \
		echo "Error: pyproject.toml not found" && exit 1; \
	fi
	@$(GET_VERSION) || (echo "Error: Failed to read version from pyproject.toml" && exit 1)

bump: ## Bump version based on conventional commits
	@if [ ! -d .git ]; then \
		echo "Error: Not a git repository. Initialize git first." && exit 1; \
	fi
	@if ! command -v git >/dev/null 2>&1; then \
		echo "Error: git is not installed" && exit 1; \
	fi
	@uv run cz bump --changelog || (echo "Error: Failed to bump version" && exit 1)
	@git add pyproject.toml src/cli/__init__.py CHANGELOG.md || (echo "Error: Failed to stage files" && exit 1)
	@git commit -m "chore: bump version to $(shell $(GET_VERSION))" || (echo "Error: Failed to commit" && exit 1)
	@git tag $(shell $(GET_VERSION) | sed 's/^/v/') || (echo "Warning: Failed to create tag (may already exist)" && true)
	@echo "Version bumped and committed. Don't forget to push with: git push --follow-tags"

bump-patch: ## Bump patch version (0.0.0 -> 0.0.1)
	@if [ ! -d .git ]; then \
		echo "Error: Not a git repository. Initialize git first." && exit 1; \
	fi
	@if ! command -v git >/dev/null 2>&1; then \
		echo "Error: git is not installed" && exit 1; \
	fi
	@uv run cz bump --increment PATCH --changelog || (echo "Error: Failed to bump version" && exit 1)
	@git add pyproject.toml src/cli/__init__.py CHANGELOG.md || (echo "Error: Failed to stage files" && exit 1)
	@git commit -m "chore: bump version to $(shell $(GET_VERSION))" || (echo "Error: Failed to commit" && exit 1)
	@git tag $(shell $(GET_VERSION) | sed 's/^/v/') || (echo "Warning: Failed to create tag (may already exist)" && true)
	@echo "Patch version bumped and committed. Don't forget to push with: git push --follow-tags"

bump-minor: ## Bump minor version (0.0.0 -> 0.1.0)
	@if [ ! -d .git ]; then \
		echo "Error: Not a git repository. Initialize git first." && exit 1; \
	fi
	@if ! command -v git >/dev/null 2>&1; then \
		echo "Error: git is not installed" && exit 1; \
	fi
	@uv run cz bump --increment MINOR --changelog || (echo "Error: Failed to bump version" && exit 1)
	@git add pyproject.toml src/cli/__init__.py CHANGELOG.md || (echo "Error: Failed to stage files" && exit 1)
	@git commit -m "chore: bump version to $(shell $(GET_VERSION))" || (echo "Error: Failed to commit" && exit 1)
	@git tag $(shell $(GET_VERSION) | sed 's/^/v/') || (echo "Warning: Failed to create tag (may already exist)" && true)
	@echo "Minor version bumped and committed. Don't forget to push with: git push --follow-tags"

bump-major: ## Bump major version (0.0.0 -> 1.0.0)
	@if [ ! -d .git ]; then \
		echo "Error: Not a git repository. Initialize git first." && exit 1; \
	fi
	@if ! command -v git >/dev/null 2>&1; then \
		echo "Error: git is not installed" && exit 1; \
	fi
	@uv run cz bump --increment MAJOR --changelog || (echo "Error: Failed to bump version" && exit 1)
	@git add pyproject.toml src/cli/__init__.py CHANGELOG.md || (echo "Error: Failed to stage files" && exit 1)
	@git commit -m "chore: bump version to $(shell $(GET_VERSION))" || (echo "Error: Failed to commit" && exit 1)
	@git tag $(shell $(GET_VERSION) | sed 's/^/v/') || (echo "Warning: Failed to create tag (may already exist)" && true)
	@echo "Major version bumped and committed. Don't forget to push with: git push --follow-tags"
