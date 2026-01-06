#!/usr/bin/env python3
"""
Project Initialization Script

Initializes a new project from the python-template.
Creates a clean git history and customizes project details.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import subprocess
import sys

# Constants
TEMPLATE_NAME = "python-template"
TEMPLATE_DESCRIPTION = "A modern Python project template"
DEFAULT_DESCRIPTION = "A modern Python project"
DEFAULT_COMMIT_MSG = "chore: initialize repository"

# Python version configuration
# This is the single source of truth for the default Python version.
# To bump the version, update this constant and the template's pyproject.toml
# (requires-python, [tool.ruff] target-version, and [tool.mypy] python_version)
DEFAULT_PYTHON_VERSION = "3.13"

# Required files for template validation
REQUIRED_FILES = [
  "pyproject.toml",
  "src/cli/main.py",
  "Makefile",
  ".pre-commit-config.yaml",
]

# Template files to remove during cleanup
TEMPLATE_CLEANUP_FILES = [
  "init_project.py",
  "CHANGELOG.md",
  "LICENSE",
]

# MkDocs files to remove if not keeping
MKDOCS_FILES = [
  "mkdocs.yml",
  "docs/",
]


@dataclass
class ProjectConfig:
  """Configuration for the new project."""

  name: str
  description: str
  author: str
  commit_msg: str
  keep_mkdocs: bool
  cleanup_template: bool
  install_dependencies: bool
  python_version: str


def print_banner() -> None:
  """Print a welcome banner."""
  print("=" * 60)
  print("🚀 Python Template Project Initializer")
  print("=" * 60)
  print()


def validate_template() -> bool:
  """Validate that we're running from a template repository."""
  missing_files = [f for f in REQUIRED_FILES if not Path(f).exists()]

  if missing_files:
    print("❌ Error: This doesn't appear to be a python-template repository.")
    print(f"Missing required files: {', '.join(missing_files)}")
    return False

  # Verify git repository exists
  if not Path(".git").exists():
    print("❌ Error: Not a git repository. Please clone the template first.")
    return False

  return True


def validate_project_name(name: str) -> bool:
  """Validate project name format."""
  if not name:
    return False
  return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))


def validate_author_email(author: str) -> bool:
  """Validate author email format."""
  if not author or "<" not in author or ">" not in author:
    return True  # Allow empty or simple names

  email_part = author.split("<")[1].split(">")[0].strip()
  return "@" in email_part and "." in email_part.split("@")[1]


def get_choice_input(prompt: str, options: list[str], error_msg: str) -> int:
  """Get a choice input from user."""
  while True:
    choice = input(f"{prompt} ").strip()
    if choice in [str(i) for i in range(1, len(options) + 1)]:
      return int(choice)
    print(f"❌ {error_msg}")


def get_user_input() -> ProjectConfig:
  """Get user input for project customization."""
  print("Let's customize your new project!")
  print()

  # Collect project name
  while True:
    project_name = input(
      "📝 Enter your project name (e.g., 'my-awesome-project'): "
    ).strip()

    if not project_name:
      print("❌ Project name cannot be empty. Please try again.")
      continue

    if not validate_project_name(project_name):
      print(
        "❌ Project name can only contain letters, numbers, hyphens, and underscores."
      )
      continue

    break

  # Collect project description
  project_description = input(
    f"📝 Enter project description (default: '{DEFAULT_DESCRIPTION}'): "
  ).strip()
  if not project_description:
    project_description = DEFAULT_DESCRIPTION

  # Collect author information
  print()
  while True:
    author = input(
      "👤 Enter your name and email (optional, press Enter to skip): "
    ).strip()

    if not author:
      break

    if not validate_author_email(author):
      print(
        "❌ Invalid email format. Please use 'Name <email@domain.com>' or press Enter to skip."
      )
      continue

    break

  # Collect commit message
  commit_msg = input(
    f"📝 Enter initial commit message (default: '{DEFAULT_COMMIT_MSG}'): "
  ).strip()
  if not commit_msg:
    commit_msg = DEFAULT_COMMIT_MSG

  # Prompt for MkDocs preference
  print()
  print("📚 Documentation options:")
  print("1. Keep MkDocs (recommended for most projects)")
  print("2. Remove MkDocs (if you prefer other documentation tools)")

  mkdocs_choice = get_choice_input(
    "Choose documentation option (1 or 2):",
    ["Keep MkDocs", "Remove MkDocs"],
    "Please enter 1 or 2.",
  )
  keep_mkdocs = mkdocs_choice == 1

  # Prompt for cleanup preference
  print()
  print("🧹 Template cleanup options:")
  print("1. Remove template-specific files (recommended)")
  print("2. Keep all files")

  cleanup_choice = get_choice_input(
    "Choose cleanup option (1 or 2):",
    ["Remove template files", "Keep all files"],
    "Please enter 1 or 2.",
  )
  cleanup_template = cleanup_choice == 1

  # Prompt for dependency installation
  print()
  print("📦 Dependency installation:")
  print("1. Run 'uv sync' now (recommended)")
  print("2. Skip dependency installation")

  install_choice = get_choice_input(
    "Install dependencies now? (1 or 2):",
    ["Install dependencies", "Skip installation"],
    "Please enter 1 or 2.",
  )
  install_dependencies = install_choice == 1

  python_version = DEFAULT_PYTHON_VERSION

  return ProjectConfig(
    name=project_name,
    description=project_description,
    author=author,
    commit_msg=commit_msg,
    keep_mkdocs=keep_mkdocs,
    cleanup_template=cleanup_template,
    install_dependencies=install_dependencies,
    python_version=python_version,
  )


def confirm_changes(config: ProjectConfig) -> bool:
  """Display summary and confirm changes before proceeding."""
  print()
  print("📋 Summary of changes:")
  print("=" * 40)
  print(f"Project name: {config.name}")
  print(f"Description: {config.description}")
  print(f"Author: {config.author if config.author else 'Not specified'}")
  print(f"Python version: {config.python_version}")
  print(f"Commit message: {config.commit_msg}")
  print(f"Keep MkDocs: {'Yes' if config.keep_mkdocs else 'No'}")
  print(f"Cleanup template files: {'Yes' if config.cleanup_template else 'No'}")
  print(f"Install dependencies: {'Yes' if config.install_dependencies else 'No'}")
  print("=" * 40)
  print()

  while True:
    confirm = input("Proceed with initialization? (y/N): ").strip().lower()
    if confirm in ["y", "yes"]:
      return True
    elif confirm in ["n", "no", ""]:
      return False
    print("❌ Please enter 'y' for yes or 'n' for no.")


class FileUpdater:
  """Manages file updates with consistent patterns."""

  @staticmethod
  def format_project_title(project_name: str) -> str:
    """Format project name as a title."""
    return project_name.replace("-", " ").title()

  @staticmethod
  def update_file(file_path: str, replacements: list[tuple[str, str]]) -> None:
    """Update a file with multiple replacements."""
    path = Path(file_path)
    content = path.read_text()

    for pattern, replacement in replacements:
      content = re.sub(pattern, replacement, content)

    path.write_text(content)
    print(f"✅ Updated {file_path}")

  @staticmethod
  def update_pyproject_toml(config: ProjectConfig) -> None:
    """Update pyproject.toml with new project details."""
    replacements = [
      (r'name = "python-template"', f'name = "{config.name}"'),
      (
        r'description = "A modern Python project template"',
        f'description = "{config.description}"',
      ),
    ]

    if config.author:
      replacements.append(
        (
          r'authors = \["Your Name <your\.email@example\.com>"\]',
          f'authors = ["{config.author}"]',
        )
      )

    FileUpdater.update_file("pyproject.toml", replacements)

  @staticmethod
  def update_makefile(config: ProjectConfig) -> None:
    """Update Makefile with new project name."""
    replacements = [
      (r"PACKAGE_NAME \?= python-template", f"PACKAGE_NAME ?= {config.name}"),
      (r"SCRIPT_NAME \?= python-template", f"SCRIPT_NAME ?= {config.name}"),
    ]
    FileUpdater.update_file("Makefile", replacements)

  @staticmethod
  def update_readme(config: ProjectConfig) -> None:
    """Update README.md with new project name."""
    project_title = FileUpdater.format_project_title(config.name)
    replacements = [
      (r"# Python Project Template", f"# {project_title}"),
      (r"poetry run python-template", f"uv run {config.name}"),
      (r"make run\s+# Default package name", f"make run  # Run {config.name}"),
    ]
    FileUpdater.update_file("README.md", replacements)

  @staticmethod
  def update_cli_script(config: ProjectConfig) -> None:
    """Update the CLI script name in pyproject.toml."""
    replacements = [
      (
        r'python-template = "src\.cli\.main:main"',
        f'{config.name} = "src.cli.main:main"',
      ),
    ]
    FileUpdater.update_file("pyproject.toml", replacements)

  @staticmethod
  def update_cli_module(config: ProjectConfig) -> None:
    """Update the CLI module with project details."""
    replacements = [
      (r'PROJECT_NAME = "python-template"', f'PROJECT_NAME = "{config.name}"'),
      (
        r'PROJECT_DESCRIPTION = "A modern Python project template"',
        f'PROJECT_DESCRIPTION = "{config.description}"',
      ),
    ]
    FileUpdater.update_file("src/cli/main.py", replacements)

  @staticmethod
  def update_mkdocs_config(config: ProjectConfig) -> None:
    """Update mkdocs.yml with project details."""
    project_title = FileUpdater.format_project_title(config.name)
    replacements = [
      (
        r"site_name: Python Project Template",
        f"site_name: {project_title}",
      ),
      (
        r"site_description: A modern Python project template with best practices",
        f"site_description: {config.description} with best practices",
      ),
      (
        r"site_url: https://your-username\.github\.io/python-template",
        f"site_url: https://your-username.github.io/{config.name}",
      ),
      (
        r"repo_name: your-username/python-template",
        f"repo_name: your-username/{config.name}",
      ),
      (
        r"repo_url: https://github\.com/your-username/python-template",
        f"repo_url: https://github.com/your-username/{config.name}",
      ),
    ]

    if config.author:
      replacements.append(
        (
          r"site_author: Your Name",
          f"site_author: {config.author.split('<')[0].strip()}",
        )
      )

    FileUpdater.update_file("mkdocs.yml", replacements)

  @staticmethod
  def remove_mkdocs_files() -> None:
    """Remove MkDocs-related files."""
    for file_path in MKDOCS_FILES:
      if Path(file_path).exists():
        if Path(file_path).is_dir():
          shutil.rmtree(file_path)
          print(f"🗑️  Removed directory: {file_path}")
        else:
          Path(file_path).unlink()
          print(f"🗑️  Removed file: {file_path}")

  @staticmethod
  def _python_version_to_ruff_format(version: str) -> str:
    """Convert Python version (e.g., '3.13') to Ruff format (e.g., 'py313')."""
    # Remove dots and add 'py' prefix
    return f"py{version.replace('.', '')}"

  @staticmethod
  def update_python_version(config: ProjectConfig) -> None:
    """Update Python version in .python-version and pyproject.toml."""
    # Update .python-version file
    Path(".python-version").write_text(f"{config.python_version}\n")
    print(f"✅ Updated .python-version to Python {config.python_version}")

    # Convert version for Ruff format (e.g., "3.13" -> "py313")
    ruff_version = FileUpdater._python_version_to_ruff_format(config.python_version)

    # Update pyproject.toml: requires-python, ruff target-version, and mypy python_version
    replacements = [
      # Update requires-python
      (
        r'requires-python = ">=\d+\.\d+,<4\.0"',
        f'requires-python = ">={config.python_version},<4.0"',
      ),
      # Update Ruff target-version
      (
        r'target-version = "py\d+"',
        f'target-version = "{ruff_version}"',
      ),
      # Update MyPy python_version
      (
        r'python_version = "\d+\.\d+"',
        f'python_version = "{config.python_version}"',
      ),
    ]
    FileUpdater.update_file("pyproject.toml", replacements)

  @staticmethod
  def _generate_readme_content(config: ProjectConfig) -> str:
    """Generate README content from template."""
    project_title = FileUpdater.format_project_title(config.name)

    return f"""# {project_title}

{config.description}

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

### CLI Usage

The template includes a CLI built with Typer:

```bash
# Show project information
uv run {config.name}

# Show help
uv run {config.name} --help

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
- `make bump-patch` - Patch version bump (0.0.0 -> 0.0.1)
- `make bump-minor` - Minor version bump (0.0.0 -> 0.1.0)
- `make bump-major` - Major version bump (0.0.0 -> 1.0.0)

### Commit Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
"""

  @staticmethod
  def create_new_readme(config: ProjectConfig) -> None:
    """Create a new README with project-specific content."""
    readme_content = FileUpdater._generate_readme_content(config)

    try:
      Path("README.md").write_text(readme_content, encoding="utf-8")
      print("✅ Created new README.md")
    except OSError as e:
      print(f"❌ Failed to create README.md: {e}")
      raise

  @staticmethod
  def cleanup_template_files(config: ProjectConfig) -> None:
    """Remove template-specific files and create new README."""
    # Create new README first
    FileUpdater.create_new_readme(config)

    # Then remove template files
    for file_path in TEMPLATE_CLEANUP_FILES:
      try:
        if Path(file_path).exists():
          Path(file_path).unlink()
          print(f"🗑️  Removed template file: {file_path}")
      except OSError as e:
        print(f"⚠️  Warning: Failed to remove {file_path}: {e}")
        # Continue with other files even if one fails


def install_dependencies() -> None:
  """Install project dependencies using uv."""
  print()
  print("📦 Installing dependencies...")

  try:
    subprocess.run(["uv", "sync", "--extra", "dev"], check=True)
    print("✅ Dependencies installed successfully")
  except subprocess.CalledProcessError as e:
    print(f"❌ Failed to install dependencies: {e}")
    print("💡 You can run 'uv sync' manually later.")
  except FileNotFoundError:
    print("❌ uv not found. Please install uv first.")
    print("💡 Visit: https://docs.astral.sh/uv/getting-started/installation/")


def create_clean_git_history(commit_msg: str) -> None:
  """Create a clean git history with a single initial commit."""
  print()
  print("🔄 Creating clean git history...")

  # Remove existing git history
  shutil.rmtree(".git")
  print("✅ Removed existing git history")

  # Initialize git repository
  subprocess.run(["git", "init"], check=True)
  print("✅ Initialized new git repository")

  # Stage all files
  subprocess.run(["git", "add", "."], check=True)
  print("✅ Staged all files")

  # Create initial commit
  subprocess.run(["git", "commit", "-m", commit_msg], check=True)
  print(f"✅ Created initial commit: '{commit_msg}'")


def show_next_steps(
  project_name: str, keep_mkdocs: bool, dependencies_installed: bool
) -> None:
  """Show next steps to the user."""
  print()
  print("🎉 Project initialization complete!")
  print("=" * 60)
  print()
  print("Next steps:")
  print()

  step_num = 1

  if not dependencies_installed:
    print(f"{step_num}. 📦 Install dependencies:")
    print("   uv sync --extra dev")
    print()
    step_num += 1

  print(f"{step_num}. 🔧 Set up pre-commit hooks:")
  print("   uv run pre-commit install")
  print()
  step_num += 1

  print(f"{step_num}. 🧪 Run tests:")
  print("   uv run pytest")
  print("   # or use: make test")
  print()
  step_num += 1

  print(f"{step_num}. 🚀 Run your application:")
  print(f"   uv run {project_name}")
  print("   # or use: make run")
  print()
  step_num += 1

  if keep_mkdocs:
    print(f"{step_num}. 📚 Build documentation:")
    print("   make docs")
    print()
    step_num += 1

  print(f"{step_num}. 🔗 Add remote repository (optional):")
  print("   git remote add origin <your-repo-url>")
  print("   git push -u origin main")
  print()
  print("Happy coding! 🚀")


def main() -> None:
  """Main function."""
  print_banner()

  # Validate template repository
  if not validate_template():
    sys.exit(1)

  # Collect user input
  config = get_user_input()

  # Confirm changes before proceeding
  if not confirm_changes(config):
    print("❌ Initialization cancelled.")
    sys.exit(0)

  print()
  print("🔄 Initializing project...")
  print()

  try:
    # Update configuration files
    FileUpdater.update_pyproject_toml(config)
    FileUpdater.update_makefile(config)
    FileUpdater.update_cli_script(config)
    FileUpdater.update_cli_module(config)
    FileUpdater.update_python_version(config)

    # Update or remove MkDocs based on user preference
    if config.keep_mkdocs:
      FileUpdater.update_mkdocs_config(config)
    else:
      FileUpdater.remove_mkdocs_files()

    # Remove template files if requested (creates new README)
    if config.cleanup_template:
      FileUpdater.cleanup_template_files(config)
    else:
      # Only update README if we're not creating a new one
      FileUpdater.update_readme(config)

    # Install dependencies if requested
    dependencies_installed = False
    if config.install_dependencies:
      install_dependencies()
      dependencies_installed = True

    # Create clean git history
    create_clean_git_history(config.commit_msg)

    # Display next steps
    show_next_steps(config.name, config.keep_mkdocs, dependencies_installed)

  except KeyboardInterrupt:
    print("\n❌ Initialization cancelled by user.")
    sys.exit(1)
  except subprocess.CalledProcessError as e:
    print(f"❌ Git command failed: {e}")
    print("💡 Make sure git is installed and you have write permissions.")
    sys.exit(1)
  except PermissionError as e:
    print(f"❌ Permission error: {e}")
    print("💡 Make sure you have write permissions to the current directory.")
    sys.exit(1)
  except Exception as e:
    print(f"❌ Unexpected error during initialization: {e}")
    print("💡 Please check the error message and try again.")
    sys.exit(1)


if __name__ == "__main__":
  main()
