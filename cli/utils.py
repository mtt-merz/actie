from inspect import getabsfile
from os import getcwd, listdir
from os.path import join as join_paths, exists
import typer


def get_path(module) -> str:
    return getabsfile(module).removesuffix("/__init__.py")


def get_actors() -> list[str]:
    return listdir(join_paths(getcwd(), "src", "actors"))


def check_project_validity(is_build_required: bool = False) -> None:
    if not exists(join_paths(getcwd(), "README.md")):
        typer.echo("Please run 'actie create' first.")
        raise typer.Exit()
    
    if is_build_required and not exists(join_paths(getcwd(), 'build')):
        typer.echo("Please run 'actie build' first.")
        raise typer.Exit()
