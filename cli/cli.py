"""This module provides the Actie CLI."""

import inspect
import os
import shutil
from typing import Optional
import typer
from distutils.dir_util import copy_tree

import actie
from examples import counter as example


app = typer.Typer()


@app.command()
def create(name: str = typer.Argument(...)) -> None:
    """Create a new Actie project."""

    path = os.path.join(os.getcwd(), name)

    if (os.path.exists(path)):
        # TODO: Cut this off, when not in development
        shutil.rmtree(path)
        # typer.echo(
        #     f"Project '{name}' already exists. Try with a different name.")
        # raise typer.Exit()

    os.mkdir(path)

    # Create README
    with open(os.path.join(path, "README.md"), "w") as f:
        f.write("# Your Actie project\n")
        f.write("Type `actie run` from the root of the project to deploy.")

    # Copy Actie module
    copy_tree(inspect.getabsfile(actie).removesuffix(
        "/__init__.py"), os.path.join(path, "actie"))

    # Create src folder and copy sample actor
    copy_tree(inspect.getabsfile(example).removesuffix(
        "/__init__.py"), os.path.join(path, "src"))

    typer.echo(f"Project '{name}' created.")
    raise typer.Exit()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{actie.__app_name__} v{actie.__version__}")
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
