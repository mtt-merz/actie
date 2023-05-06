from inspect import getabsfile


def get_path(module) -> str:
    return getabsfile(module).removesuffix("/__init__.py")