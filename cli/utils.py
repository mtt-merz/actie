from inspect import getabsfile
from os import getcwd, listdir
from os.path import join as join_paths

def get_path(module) -> str:
    return getabsfile(module).removesuffix("/__init__.py")


def get_actors() -> list[str]:
    return listdir(join_paths(getcwd(), "src", "actors"))
