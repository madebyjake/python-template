#!/bin/bash
# Setup script for development environment

set -euo pipefail

# Ensure script is run from project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if we're in the project root
if [ "$(pwd)" != "$PROJECT_ROOT" ]; then
    echo "This script must be run from the project root directory."
    echo "Current directory: $(pwd)"
    echo "Project root: $PROJECT_ROOT"
    echo "Please run: cd $PROJECT_ROOT && ./scripts/$(basename "$0")"
    exit 1
fi

# Default values
INSTALL_DEV=false  # Default to base-only
INSTALL_HOOKS=true
INTERACTIVE=false  # Default to non-interactive

# Function to display usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -h, --help                 Display this help message"
    echo "  -b, --base-only            Install only base dependencies (default)"
    echo "  -d, --with-dev             Install with dev dependencies"
    echo "  -n, --no-hooks             Skip installation of pre-commit hooks"
    echo "  -i, --interactive          Run in interactive mode with prompts"
    echo
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -b|--base-only)
            INSTALL_DEV=false
            shift
            ;;
        -d|--with-dev)
            INSTALL_DEV=true
            shift
            ;;
        -n|--no-hooks)
            INSTALL_HOOKS=false
            shift
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install it first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Interactive mode
if [ "$INTERACTIVE" = true ]; then
    # Ask about dev dependencies
    read -p "Install development dependencies? (y/N): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        INSTALL_DEV=true
    else
        INSTALL_DEV=false
    fi

    # Ask about pre-commit hooks
    read -p "Install pre-commit hooks? (Y/n): " answer
    if [[ "$answer" =~ ^[Nn]$ ]]; then
        INSTALL_HOOKS=false
    else
        INSTALL_HOOKS=true
    fi
fi

# Install dependencies
if [ "$INSTALL_DEV" = true ]; then
    echo "Installing all dependencies (including dev)..."
    poetry install
else
    echo "Installing base dependencies only (no dev)..."
    poetry install --only main
fi

# Install pre-commit hooks
if [ "$INSTALL_HOOKS" = true ]; then
    echo "Installing pre-commit hooks..."
    if ! poetry run pre-commit install; then
        echo "Warning: Failed to install pre-commit hooks. This might be due to dependency issues."
        echo "You can try manually installing pre-commit with: pip install pre-commit"
        echo "Then run: pre-commit install"
    else
        # Only try to install commit-msg hook if the first command succeeded
        if ! poetry run pre-commit install --hook-type commit-msg; then
            echo "Warning: Failed to install commit-msg hook, but other hooks were installed."
        else
            echo "Pre-commit hooks installed successfully."
        fi
    fi
else
    echo "Skipping pre-commit hooks installation."
fi

echo "Setup complete! You can now start developing."

# Print a summary of what was installed
echo
echo "Installation Summary:"
if [ "$INSTALL_DEV" = true ]; then
    echo "✓ Installed all dependencies (including development dependencies)"
else
    echo "✓ Installed base dependencies only"
fi

if [ "$INSTALL_HOOKS" = true ]; then
    if [ -f ".git/hooks/pre-commit" ]; then
        echo "✓ Pre-commit hooks installed"
    else
        echo "✗ Pre-commit hooks installation failed"
    fi
else
    echo "- Pre-commit hooks skipped"
fi
