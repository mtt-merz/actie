"""This module provides the Actie CLI."""

import base64
from distutils.dir_util import copy_tree, remove_tree
import json
from os import mkdir, getcwd, chdir
from os.path import join as join_paths, exists
from shutil import rmtree, make_archive, copyfile
from typing import Optional
import typer
import venv

from cli.utils import *
from examples import collector as example
import lib
import lib.wsk
import resources
import server


app = typer.Typer()


@app.command()
def create(project_name: str = typer.Argument(...)) -> None:
    """Create a new Actie project."""
    typer.echo(f"Start creating '{project_name}' project...")

    project_path = join_paths(getcwd(), project_name)

    if (exists(project_path)):
        # TODO: Cut this off, when not in development
        rmtree(project_path)
        # typer.echo(
        #     f"Project '{project_name}' already exists. Try with a different name.")
        # raise typer.Exit()

    mkdir(project_path)
    typer.echo("Moving files...")

    # Move library
    copy_tree(
        get_path(lib),
        join_paths(project_path, "lib")
    )

    # Move sample actor
    copy_tree(
        get_path(example),
        join_paths(project_path, "src")
    )

    # Move config
    copyfile(
        join_paths(get_path(resources), "config.txt"),
        join_paths(project_path, "config.json")
    )

    typer.echo("Adding files...")

    # Create README
    readme_path = join_paths(project_path, "README.md")
    with open(readme_path, "w") as f:
        f.write("# Your Actie project\n")
        f.write("Type `actie run` from the root of the project to deploy.")

    # Create .gitignore
    gitignore_path = join_paths(project_path, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write("*.pyc\n")
        f.write("__pycache__/\n")
        f.write("build/\n")
        f.write("egg-info/\n")
        f.write(".vscode/\n")
        f.write("config.json\n")

    typer.echo(f"\nProject '{project_name}' created.")
    raise typer.Exit()


@app.command()
def build() -> None:
    """Build Actie project."""

    if not exists(join_paths(getcwd(), "README.md")):
        typer.echo("Please run 'actie create' first.")
        raise typer.Exit()

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

        # Move configs
        copyfile(
            join_paths(getcwd(), "config.json"),
            join_paths(actor_build_path, "config.json")
        )

        typer.echo("Adding files...")

        # Add {actor_build_path}/__main__.py
        main_in_path = join_paths(get_path(resources), "__main__.py")
        main_out_path = join_paths(actor_build_path, "__main__.py")
        with open(main_in_path, "r") as f_in, \
                open(main_out_path, "w") as f_out:
            code = f_in.read()
            code = code.replace("__actor__", actor)
            code = code.replace("__Actor__", actor.capitalize())

            f_out.write(code)

        # Install dependencies
        # typer.echo("Adding dependencies...")

        # venv_path = join_paths(actor_build_path, "virtualenv")
        # venv.create(venv_path, with_pip=True)
        # pip_path = join_paths(venv_path, "bin", "pip")

        # actor_req_path = join_paths(actor_build_path, "requirements.txt")
        # if exists(actor_req_path):
        #     subprocess.run([
        #         pip_path, "install",
        #         "-r", actor_req_path
        #     ])

        # subprocess.run([
        #     pip_path, "install",
        #     "-r", join_paths(get_path(lib), "requirements.txt")
        # ])

        typer.echo(f"Actor '{actor}' built")


@app.command()
def run(local: bool = typer.Option(False, "--local", "-l")) -> None:
    """Run Actie project."""
    build()

    with open(join_paths(getcwd(), "config.json"), "r") as f:
        config = json.loads(f.read())["wsk"]

    wsk = lib.wsk.LocalOpenWhisk() if local else lib.wsk.OpenWhisk(
        config["host"], config["auth"])

    # Deploy actors to OpenWhisk
    for actor in get_actors():
        typer.echo(f"Deploying actor '{actor}'...")

        actor_build_path = join_paths(getcwd(), "build", actor)

        # Set proper OpenWhiskInterface
        with open(join_paths(actor_build_path, "__main__.py"), "r+") as f:
            code = f.read()
            code = code.replace("__local__: bool", "")
            code = code.replace("__local__", str(local))

            f.seek(0)
            f.truncate()
            f.write(code)

        # Archive all files
        archive_path = make_archive(
            join_paths(actor_build_path, actor), "zip",
            root_dir=actor_build_path
        )

        # Deploy actors
        with open(archive_path, "rb") as f:
            code = base64.b64encode(f.read())
            code = code.decode("utf-8")
            res = wsk.create(actor, code)

        if not local and "error" in res.keys():
            if "already exists" in res["error"]:
                typer.echo("Actor already deployed")
            else:
                raise Exception(res["error"])

        else:
            typer.echo("Actor deployed")

            if not local:
                code = res["exec"]["code"]
                code = code[:100] + f"...({len(code) - 200} chars dropped)"
                res["exec"]["code"] = code
                typer.echo(json.dumps(res, indent=2))

    # Execute entrypoint
    typer.echo("\nStart running project...")
    main_path = join_paths(getcwd(), "src", "__main__.py")
    with open(main_path, "r") as f:
        compiled_code = compile(f.read(), "<string>", "exec")
        exec(compiled_code)


@app.command()
def clean() -> None:
    """Clean Actie project."""

    build_path = join_paths(getcwd(), "build")
    if exists(build_path):
        remove_tree(build_path)

    typer.echo("Project cleaned")


@app.command()
def serve() -> None:
    """Serve Actie project."""

    snapshot_path = join_paths(getcwd(), "snapshots")
    if not exists(snapshot_path):
        mkdir(snapshot_path)

    chdir(snapshot_path)

    with open(join_paths(get_path(server), "__main__.py"), "r") as f:
        exec(f.read())


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
