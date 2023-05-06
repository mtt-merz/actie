"""This module provides the Actie CLI."""

import base64
import json
import os
from shutil import rmtree, make_archive, copyfile
from typing import Optional
import typer
from distutils.dir_util import copy_tree

import libs
import libs.actie as actie
import libs.wsk
import utils
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

    # Copy libraries
    copy_tree(get_module_path(libs), os.path.join(path, "libs"))
    typer.echo("Copy libraries")

    # Create wsk_config.json
    with open(os.path.join(path, "wsk_config.json"), "w") as f:
        config = {"api_host": "API_HOST", "auth": "AUTH"}
        f.write(json.dumps(config))

    # Create src folder and sample actor
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

    with open(os.path.join(os.getcwd(), "wsk_config.json"), "r") as f:
        config = json.loads(f.read())
        wsk = libs.wsk.OpenWhisk(config["api-host"], config["auth"])

    build_path = os.path.join(os.getcwd(), "build")
    os.mkdir(build_path)

    for actor in actors:
        typer.echo(actor.upper())

        actor_build_path = os.path.join(build_path, actor)
        os.mkdir(actor_build_path)

        # Add {actor_build_path}/__main__.py
        with open(os.path.join(get_module_path(utils), "__main__.py"), "r") as fin, \
                open(os.path.join(actor_build_path, "__main__.py"), "w") as fout:
            code = fin.read()
            code = code.replace("__actor__", actor)
            code = code.replace("__Actor__", actor.capitalize())
            
            fout.write(code)

        # Add wsk_config.json
        copyfile(os.path.join(os.getcwd(), "wsk_config.json"),
                 os.path.join(actor_build_path, "wsk_config.json"))

        # Add actor code
        actor_path = os.path.join(os.getcwd(), "src", "actors", actor)
        copy_tree(actor_path, actor_build_path)

        # Add libraries
        copy_tree(get_module_path(libs), os.path.join(
            actor_build_path, "libs"))

        # Archive all files
        archive_path = make_archive(
            actor_build_path, "zip",
            root_dir=actor_build_path
        )
        typer.echo(f"Create archive")

        # Deploy actor to OpenWhisk
        with open(archive_path, 'rb') as file:
            code = base64.b64encode(file.read())
            wsk.create(actor, code)

        # rmtree(build_path)
        typer.echo(f"Create OpenWhisk action")
        
        # Execute main
        typer.echo("\nRunning main...")
        with open(os.path.join(os.getcwd(), "src", "__main__.py"), "r") as f:
            code = f.read()
            exec(code)


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
