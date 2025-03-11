# `python-template`

## Features

- [Poetry](https://python-poetry.org/) for dependency management and packaging
- Modern Python support (3.10-3.13)
- Comprehensive code quality tools:
  - [Black](https://black.readthedocs.io/) for consistent code formatting
  - [isort](https://pycqa.github.io/isort/) for standardized import ordering
  - [Flake8](https://flake8.pycqa.org/) for code style and quality checking
    - flake8-bandit for security checks
    - flake8-bugbear for additional bug checks
    - flake8-docstrings for docstring validation
    - flake8-isort for import ordering
  - [mypy](https://mypy.readthedocs.io/) for static type checking
  - [Bandit](https://bandit.readthedocs.io/) for security linting
- Testing infrastructure:
  - [pytest](https://docs.pytest.org/) for testing
  - [pytest-cov](https://pytest-cov.readthedocs.io/) for code coverage reporting
  - Configured minimum 70% code coverage requirement
- Git hooks and commit standards:
  - [pre-commit](https://pre-commit.com/) for automated git hooks
  - [Conventional Commits](https://www.conventionalcommits.org/) standard using commitizen
- Development environment:
  - Preconfigured VSCode settings (`.vscode/settings.json`) and extension recommendations (`.vscode/extensions.json`).
  - Setup script (`scripts/setup.sh`) with options for:
    - Installing base or development dependencies
    - Configuring pre-commit hooks
    - Interactive or non-interactive mode
