"""Tests for the CLI module."""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import MagicMock

import pytest

from src.cli.main import (
  PROJECT_DESCRIPTION,
  PROJECT_NAME,
  app,
  cli,
  info,
  main,
  version,
)


@pytest.fixture
def output_stream() -> StringIO:
  """Fixture providing a StringIO output stream."""
  return StringIO()


@pytest.fixture
def mock_context() -> MagicMock:
  """Fixture providing a mock Typer context."""
  ctx = MagicMock()
  ctx.invoked_subcommand = None
  return ctx


@pytest.fixture
def expected_version() -> str:
  """Fixture providing the expected version string."""
  return "0.0.0"


class TestCLIImports:
  """Test cases for CLI imports and basic structure."""

  def test_cli_imports(self) -> None:
    """Test that CLI functions can be imported."""
    assert callable(cli)
    assert callable(version)
    assert callable(info)
    assert app is not None

  def test_project_constants(self) -> None:
    """Test that project constants are properly defined."""
    assert isinstance(PROJECT_NAME, str)
    assert isinstance(PROJECT_DESCRIPTION, str)
    assert len(PROJECT_NAME) > 0
    assert len(PROJECT_DESCRIPTION) > 0


class TestCLICommands:
  """Test cases for CLI command functions."""

  @pytest.mark.parametrize(
    ("command_func", "expected_content"),
    [
      (version, f"{PROJECT_NAME} version 0.0.0"),
      (info, PROJECT_NAME),
    ],
  )
  def test_command_output_contains_expected(
    self, output_stream: StringIO, command_func, expected_content: str
  ) -> None:
    """Test that command functions output expected content."""
    with redirect_stdout(output_stream):
      command_func()

    result = output_stream.getvalue()
    assert expected_content in result

  def test_main_function_direct(
    self, output_stream: StringIO, mock_context: MagicMock
  ) -> None:
    """Test main function called directly."""
    with redirect_stdout(output_stream):
      main(mock_context, version_flag=False)

    result = output_stream.getvalue()
    assert PROJECT_NAME in result
    assert PROJECT_DESCRIPTION in result
    assert "Version: 0.0.0" in result
    assert "Use --help" in result

  def test_version_output_format(
    self, output_stream: StringIO, expected_version: str
  ) -> None:
    """Test version output format."""
    with redirect_stdout(output_stream):
      version()

    result = output_stream.getvalue().strip()
    assert result == f"{PROJECT_NAME} version {expected_version}"

  def test_info_output_contains_required_info(
    self, output_stream: StringIO, expected_version: str
  ) -> None:
    """Test that info output contains all required information."""
    with redirect_stdout(output_stream):
      info()

    result = output_stream.getvalue()
    lines = result.strip().split("\n")

    assert len(lines) == 3
    assert lines[0] == PROJECT_NAME
    assert lines[1] == PROJECT_DESCRIPTION
    assert lines[2] == f"Version: {expected_version}"

  @pytest.mark.parametrize(
    ("command_func", "expected_strings"),
    [
      (info, [PROJECT_NAME, PROJECT_DESCRIPTION, "Version: 0.0.0"]),
      (version, [PROJECT_NAME, "version", "0.0.0"]),
    ],
  )
  def test_command_output_contains_multiple_strings(
    self,
    output_stream: StringIO,
    command_func,
    expected_strings: list[str],
  ) -> None:
    """Test that command outputs contain multiple expected strings."""
    with redirect_stdout(output_stream):
      command_func()

    result = output_stream.getvalue()
    for expected_string in expected_strings:
      assert expected_string in result, (
        f"Expected '{expected_string}' not found in output"
      )
