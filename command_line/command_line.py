"""This module provides the Actie CLI."""

import inspect
import os
from typing import Optional
import typer

from actie import __app_name__, __version__, Actor
from actie.samples.counter import Counter


app = typer.Typer()


@app.command()
def create(name: str = typer.Argument(...)) -> None:
    """Create a new Actie project."""

    path = os.path.join(os.getcwd(), name)

    if (os.path.exists(path)):
        typer.echo(
            f"Project '{name}' already exists. Try with a different name.")
        raise typer.Exit()

    os.mkdir(path)

    # Create README
    with open(os.path.join(path, "README.md"), "w") as f:
        f.write("# Your Actie project\n")
        f.write("Type `actie run` from the root of the project to deploy.")

    # Create Actie module
    os.mkdir(os.path.join(path, 'actie'))

    with open(os.path.join(path, 'actie', '__init__.py'), 'w') as f:
        f.write("")

    with open(os.path.join(path, 'actie', 'actor.py'), 'w') as f:
        f.write(inspect.getsource(Actor))

    # Create src folder and sample actor
    os.mkdir(os.path.join(path, 'src'))

    with open(os.path.join(path, 'src', 'counter.py'), 'w') as f:
        f.write(inspect.getsource(Counter))

    typer.echo(f"Project '{name}' created.")
    raise typer.Exit()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
