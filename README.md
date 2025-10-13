# Python Project Template

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-FFD43B?logo=uv&logoColor=000)](https://docs.astral.sh/uv/)
[![Typer](https://img.shields.io/badge/Typer-FF6B6B?logo=python&logoColor=white)](https://typer.tiangolo.com/)
[![Ruff](https://img.shields.io/badge/Ruff-7C3AED?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)
[![mypy](https://img.shields.io/badge/mypy-1976D2?logo=python&logoColor=white)](https://mypy.readthedocs.io/)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=python&logoColor=white)](https://pytest.org/)
[![MkDocs](https://img.shields.io/badge/MkDocs-526CFE?logo=materialformkdocs&logoColor=fff)](https://www.mkdocs.org/)
[![Make](https://img.shields.io/badge/Make-FF8C00?logo=gnu&logoColor=white)](https://www.gnu.org/software/make/)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative&logoColor=white)](LICENSE)

A Python project template with modern tooling, automated testing, security scanning, documentation generation, and CLI functionality.

## Includes

- **Ruff** - Linter and code formatter
- **uv** - Fast Python package and project manager
- **mypy** - Static type checking
- **pytest** - Testing framework with coverage
- **Typer** - CLI framework with automatic help generation
- **Pre-commit hooks** - Code quality automation
- **MkDocs** - Documentation with API generation
- **Security tools** - Safety and Bandit for vulnerability scanning
- **Commitizen** - Automated versioning and changelog generation
- **IDE Support** - VS Code configuration and pyenv support

## Getting Started

### Option 1: Quick Start with Clean History (Recommended)

1. Clone the template:
   ```bash
   git clone https://github.com/madebyjake/python-template.git <project-name>
   cd <project-name>
   ```

2. Run the initialization script:
   ```bash
   python init_project.py
   ```

   The script will:
   - Ask for your project name and customize all files
   - Create a clean git history with a single initial commit
   - Optionally remove template-specific files
   - Show you the next steps

3. Follow the displayed next steps to install dependencies and start building.

### Option 2: Manual Setup

1. Clone and customize:
   ```bash
   git clone https://github.com/madebyjake/python-template.git <project-name>
   cd <project-name>
   # Update pyproject.toml with your project details
   ```

2. (Optional) Create clean git history:
   ```bash
   # Remove template history and start fresh
   rm -rf .git
   git init
   git add .
   git commit -m "chore: initialize repository"
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Set up pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

5. Run tests:
   ```bash
   uv run pytest
   # Or use make commands:
   make test
   make check  # Run all checks
   ```

6. Run the application:
   ```bash
   uv run python-template
   # Or use make commands:
   make run                    # Run with default package name
   make run ARGS="--help"      # Run with arguments
   make debug                  # Run in debug mode
   ```

## Requirements

- **Python**: 3.10, 3.11, 3.12, 3.13, or 3.14
- **uv**: For dependency management

### Installing uv

Install uv with the official installer:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or install via pip:
```bash
pip install uv
```

## Development

### Development Commands

Use `make help` to see all available commands, or run directly:

**Setup & Dependencies:**
- **Setup:** `make setup` - Complete development setup (install deps + pre-commit)
- **Install:** `make install` - Install main dependencies
- **Install dev:** `make install-dev` - Install all dependencies including dev
- **Add package:** `make add PACKAGE=name` - Add a new dependency
- **Remove package:** `make remove PACKAGE=name` - Remove a dependency
- **Dependency tree:** `make tree` - Show dependency tree

**Code Quality:**
- **All checks:** `make check` - Run linting, type checking, and tests
- **Fast checks:** `make check-fast` - Run fast checks (lint only)
- **Full checks:** `make check-full` - Run all checks including coverage
- **Lint:** `make lint` - Run Ruff linter
- **Format:** `make format` - Format code with Ruff
- **Format check:** `make format-check` - Check if code is formatted correctly
- **Format fix:** `make format-fix` - Format code and fix issues automatically
- **Type check:** `make type-check` - Run mypy type checking

**Testing & Building:**
- **Test:** `make test` - Run tests
- **Test with coverage:** `make test-cov` - Run tests with coverage report
- **Build:** `make build` - Build package for distribution
- **Publish:** `make publish` - Publish to PyPI

**Application:**
- **Run:** `make run` - Run the application
- **Debug:** `make debug` - Run in debug mode

**Documentation:**
- **Build docs:** `make docs` - Build documentation
- **Serve docs:** `make serve-docs` - Serve documentation locally

**Performance:**
- **Benchmark:** `make benchmark` - Benchmark linting and formatting performance
- **Profile:** `make profile` - Profile dependency resolution

### Project Structure
```
├── src/                        # Source code
│   └── cli/                    # CLI package
│       ├── __init__.py         # Package initialization with version
│       └── main.py             # CLI module with Typer
├── tests/                      # Test files
│   ├── __init__.py
│   └── test_cli.py             # CLI tests
├── docs/                       # Documentation
│   ├── index.md
│   └── api.md
├── init_project.py             # Project initialization script
├── .vscode/                    # VSCode configuration
│   ├── settings.json           # Editor settings
│   └── extensions.json         # Recommended extensions
├── pyproject.toml              # Project configuration
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .editorconfig               # Editor configuration
├── .python-version             # Python version for pyenv
├── mkdocs.yml                  # Documentation configuration
├── Makefile                    # Development commands
├── CHANGELOG.md                # Version history
└── README.md
```

### CLI Usage

The template includes a CLI built with Typer:

```bash
# Show project information
uv run python-template

# Show help
uv run python-template --help

# Run application (multiple ways)
make run                           # Default package name
make run ARGS="--help"             # With arguments
make debug                         # Debug mode
```

### Makefile

The Makefile provides commands for installing dependencies, running tests, linting, formatting, building, publishing, and managing versioning.

- **Configurable**: Update `MAIN_MODULE` and `MAIN_FUNCTION` in Makefile for different entry points
- **Flexible**: Supports running any package with `make run <package-name>`
- **Consistent**: Same commands work regardless of application type
- **Extensible**: Easy to add new targets for different project needs

### Security

The project includes security scanning tools:

- **Safety:** `uv run safety scan` - Check for known vulnerabilities
- **Bandit:** `uv run bandit -r src/` - Security linting for Python code

## IDE Support

### VS Code
- **Settings**: Configuration in `.vscode/settings.json` with 2-space indentation, Ruff integration
- **Extensions**: Extension recommendations in `.vscode/extensions.json`
- **Python**: Uses Ruff for linting and formatting

### pyenv
- **Python Version**: Specified in `.python-version` (3.14)
- **Automatic**: pyenv will automatically use the correct Python version

## Configuration

All tools are configured in `pyproject.toml`. See the file for specific settings.

## Versioning and Changelog

The project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for automated versioning and changelog generation.

- **Versioning**: Follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)
- **Changelog**: Generated from commit messages
- **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/) format
- **Releases**: Independent of CI/CD platforms

### Versioning Commands
- `make version` - Show current version
- `make bump` - Bump version based on conventional commits
- `make bump-patch` - Patch version bump (0.0.0 → 0.0.1)
- `make bump-minor` - Minor version bump (0.0.0 → 0.1.0)
- `make bump-major` - Major version bump (0.0.0 → 1.0.0)

### Commit Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## License

MIT License - see [LICENSE](LICENSE) file for details.
