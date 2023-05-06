"""This module provides the Actie CLI."""

import base64
from distutils.dir_util import copy_tree, remove_tree
import json
from os import mkdir, getcwd
from os.path import join as join_paths, exists
from shutil import rmtree, make_archive, copyfile
import subprocess
from typing import Optional
import typer
import venv

import lib
import resources
from examples import counter as example
from cli.utils import *


app = typer.Typer()


@app.command()
def create(name: str = typer.Argument(...)) -> None:
    """Create a new Actie project."""
    typer.echo(f"Start creating '{name}' project...")

    project_path = join_paths(getcwd(), name)

    if (exists(project_path)):
        # TODO: Cut this off, when not in development
        rmtree(project_path)
        # typer.echo(
        #     f"Project '{name}' already exists. Try with a different name.")
        # raise typer.Exit()

    mkdir(project_path)
    typer.echo("Moving files...")

    # Copy libraries
    copy_tree(
        get_path(lib),
        join_paths(project_path, "lib")
    )

    # Create src folder and sample actor
    copy_tree(
        get_path(example),
        join_paths(project_path, "src")
    )

    typer.echo("Adding files...")

    # Create README
    readme_path = join_paths(project_path, "README.md")
    with open(readme_path, "w") as f:
        f.write("# Your Actie project\n")
        f.write("Type `actie run` from the root of the project to deploy.")

    # Create wsk_config.json
    wsk_config_path = join_paths(project_path, "wsk_config.json")
    with open(wsk_config_path, "w") as f:
        config = {"api-host": "API_HOST", "auth": "AUTH"}
        f.write(json.dumps(config))

    # Create .gitignore
    gitignore_path = join_paths(project_path, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write("*.pyc\n")
        f.write("__pycache__/\n")
        f.write("build/\n")
        f.write("egg-info/\n")
        f.write(".vscode/\n")

    typer.echo(f"\nProject '{name}' created.")
    raise typer.Exit()


@app.command()
def build() -> None:
    """Build Actie project."""
    typer.echo(f"Start building...")

    build_path = join_paths(getcwd(), "build")
    if (exists(build_path)):
        remove_tree(build_path)
    mkdir(build_path)

    # Detect project actors
    actors = get_actors()
    typer.echo(f"Found {len(actors)} actor(s): {', '.join(actors)}")

    for actor in actors:
        typer.echo(f"\n[{actor}]")

        typer.echo("Moving files...")

        actor_build_path = join_paths(build_path, actor)
        mkdir(actor_build_path)

        # Move actor code
        copy_tree(
            join_paths(getcwd(), "src", "actors", actor),
            actor_build_path
        )

        # Move internal libraries
        copy_tree(
            get_path(lib),
            join_paths(actor_build_path, "lib")
        )

        typer.echo("Adding files...")

        # Add {actor_build_path}/__main__.py
        main_in_path = join_paths(get_path(resources), "__main__.py")
        main_out_path = join_paths(actor_build_path, "__main__.py")
        with open(main_in_path, "r") as fin, \
                open(main_out_path, "w") as fout:
            code = fin.read()
            code = code.replace("__actor__", actor)
            code = code.replace("__Actor__", actor.capitalize())

            fout.write(code)

        # Add wsk_config.json
        copyfile(
            join_paths(getcwd(), "wsk_config.json"),
            join_paths(actor_build_path, "wsk_config.json")
        )

        # Install dependencies
        typer.echo("Adding dependencies...")
        venv.create(
            join_paths(actor_build_path, ".venv"),
            with_pip=True
        )

        actor_req_path = join_paths(actor_build_path, "requirements.txt")
        if exists(actor_req_path):
            subprocess.run([
                join_paths(actor_build_path, ".venv", "bin", "pip"),
                "install",
                "-r", actor_req_path
            ])

        subprocess.run([
            join_paths(actor_build_path, ".venv", "bin", "pip"),
            "install",
            "-r", join_paths(get_path(lib), "requirements.txt")
        ])

        # Archive all files
        archive_path = make_archive(
            join_paths(actor_build_path, actor), "zip",
            root_dir=actor_build_path
        )

        typer.echo(f"Actor '{actor}' built")


@app.command()
def run() -> None:
    """Run Actie project."""
    build()

    with open(join_paths(getcwd(), "wsk_config.json"), "r") as f:
        config = json.loads(f.read())
        wsk = lib.OpenWhisk(config["api-host"], config["auth"])

    # Deploy actors to OpenWhisk
    for actor in get_actors():
        typer.echo(f"Deploying actor '{actor}'...")

        archive_path = join_paths(getcwd(), "build", actor, f"{actor}.zip")
        with open(archive_path, 'rb') as file:
            code = base64.b64encode(file.read())
            wsk.create(actor, code)

    # Execute entrypoint
    typer.echo("\nStart running project...")
    with open(join_paths(getcwd(), "src", "__main__.py"), "r") as f:
        code = f.read()
        exec(code)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{lib.__app_name__} v{lib.__version__}")
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
