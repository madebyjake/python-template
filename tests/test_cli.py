"""Tests for the CLI module."""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import MagicMock

from src.cli.main import (
  PROJECT_DESCRIPTION,
  PROJECT_NAME,
  app,
  cli,
  info,
  main,
  version,
)


class TestCLI:
  """Test cases for CLI functionality."""

  def test_main_function_direct(self) -> None:
    """Test main function called directly."""
    output = StringIO()
    with redirect_stdout(output):
      # Create a mock context for the callback
      ctx = MagicMock()
      ctx.invoked_subcommand = None
      main(ctx, version_flag=False)

    result = output.getvalue()
    assert PROJECT_NAME in result
    assert PROJECT_DESCRIPTION in result
    assert "Version: 0.0.0" in result
    assert "Use --help" in result

  def test_version_function_direct(self) -> None:
    """Test version function called directly."""
    output = StringIO()
    with redirect_stdout(output):
      version()

    assert f"{PROJECT_NAME} version 0.0.0" in output.getvalue()

  def test_info_function_direct(self) -> None:
    """Test info function called directly."""
    output = StringIO()
    with redirect_stdout(output):
      info()

    result = output.getvalue()
    assert PROJECT_NAME in result
    assert PROJECT_DESCRIPTION in result
    assert "Version: 0.0.0" in result

  def test_cli_imports(self) -> None:
    """Test that CLI functions can be imported."""
    assert callable(cli)
    assert callable(version)
    assert callable(info)
    assert app is not None

  def test_version_output_format(self) -> None:
    """Test version output format."""
    output = StringIO()
    with redirect_stdout(output):
      version()

    result = output.getvalue().strip()
    assert result == f"{PROJECT_NAME} version 0.0.0"

  def test_info_output_contains_required_info(self) -> None:
    """Test that info output contains all required information."""
    output = StringIO()
    with redirect_stdout(output):
      info()

    result = output.getvalue()
    lines = result.strip().split("\n")

    assert len(lines) == 3
    assert lines[0] == PROJECT_NAME
    assert lines[1] == PROJECT_DESCRIPTION
    assert lines[2] == "Version: 0.0.0"

  def test_project_constants(self) -> None:
    """Test that project constants are properly defined."""
    assert isinstance(PROJECT_NAME, str)
    assert isinstance(PROJECT_DESCRIPTION, str)
    assert len(PROJECT_NAME) > 0
    assert len(PROJECT_DESCRIPTION) > 0
