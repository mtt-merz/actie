"""This module provides the Actie CLI."""

import base64
import os
from shutil import rmtree, make_archive
from typing import Optional
import typer
from distutils.dir_util import copy_tree

import actie
import exec
from examples import counter as example
from cli.utils import *


app = typer.Typer()


@app.command()
def create(name: str = typer.Argument(...)) -> None:
    """Create a new Actie project."""
    typer.echo(f"Start creating '{name}' project...\n")

    path = os.path.join(os.getcwd(), name)

    if (os.path.exists(path)):
        # TODO: Cut this off, when not in development
        rmtree(path)
        # typer.echo(
        #     f"Project '{name}' already exists. Try with a different name.")
        # raise typer.Exit()

    os.mkdir(path)

    # Create README
    with open(os.path.join(path, "README.md"), "w") as f:
        f.write("# Your Actie project\n")
        f.write("Type `actie run` from the root of the project to deploy.")
    typer.echo("Create README.md")

    # Copy Actie module
    copy_tree(get_module_path(actie), os.path.join(path, "actie"))
    typer.echo("Copy actie module")

    # Create src folder and copy sample actor
    copy_tree(get_module_path(example), os.path.join(path, "src"))
    typer.echo("Create src folder and copy example actor")

    typer.echo(f"\nProject '{name}' created.")
    raise typer.Exit()


@app.command()
def run() -> None:
    """Run an Actie project."""
    typer.echo(f"Start running...\n")

    # Detect project actors
    actors = os.listdir(os.path.join(os.getcwd(), "src", "actors"))
    
    wsk = actie.OpenWhiskAPI()

    build_path = os.path.join(os.getcwd(), "build")
    for actor in actors:
        typer.echo(actor.upper())

        actor_build_path = os.path.join(build_path, actor)

        # Add __main__ and repository
        copy_tree(get_module_path(exec), actor_build_path)

        # Add actor code
        actor_path = os.path.join(os.getcwd(), "src", "actors", actor)
        copy_tree(actor_path, actor_build_path)

        # Add actie library
        copy_tree(get_module_path(actie), os.path.join(
            actor_build_path, "actie"))

        # Archive all files
        archive_path = make_archive(
            actor_build_path, "zip",
            root_dir=actor_build_path
        )
        rmtree(actor_build_path)
        typer.echo(f"Create archive")

        # Deploy actor to OpenWhisk
        with open(archive_path, 'rb') as file:
            code = base64.b64encode(file.read())
            wsk.create(actor, code)
            
        typer.echo(f"Create OpenWhisk action")


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
