"""CLI module for the application."""

import typer

from . import __version__

PROJECT_NAME = "python-template"
PROJECT_DESCRIPTION = "A modern Python project template"

app = typer.Typer(
  name=PROJECT_NAME,
  help=PROJECT_DESCRIPTION,
  add_completion=False,
)

info_group = typer.Typer(name="info", help="Project information commands")
app.add_typer(info_group)


@app.command()
def version() -> None:
  """Show the version information."""
  typer.echo(f"{PROJECT_NAME} version {__version__}")


def _show_info() -> None:
  """Internal function to show project information."""
  typer.echo(PROJECT_NAME)
  typer.echo(PROJECT_DESCRIPTION)
  typer.echo(f"Version: {__version__}")


@info_group.callback(invoke_without_command=True)
def info_group_callback(ctx: typer.Context) -> None:
  """Project information commands."""
  if ctx.invoked_subcommand is None:
    # If no subcommand provided, show project info
    _show_info()


@info_group.command()
def show() -> None:
  """Show project information."""
  _show_info()


# Export info function for backward compatibility with tests
def info() -> None:
  """Show project information (backward compatibility)."""
  _show_info()


@app.callback(invoke_without_command=True)
def main(
  ctx: typer.Context,
  version_flag: bool = typer.Option(
    False,
    "--version",
    "-v",
    help="Show version information and exit",
  ),
) -> None:
  """Main CLI entry point."""
  if version_flag:
    version()
    raise typer.Exit()

  # If no command is provided, show default help
  if ctx.invoked_subcommand is None:
    typer.echo(f"{PROJECT_NAME} - {PROJECT_DESCRIPTION}")
    typer.echo(f"Version: {__version__}")
    typer.echo()
    typer.echo("Use --help to see available commands.")


def cli() -> None:
  """CLI entry point function."""
  app()


if __name__ == "__main__":
  cli()
