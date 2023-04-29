from setuptools import setup, find_packages
from command_line import __name__, __version__, __description__


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=readfile('README.md'),
    license=readfile('LICENSE'),
    author="Matteo Merz",
    author_email="matteo.merz@mail.polimi.it",
    url="https://github.com/mtt-merz/actie-cli",
    entry_points={
        'console_scripts': ['actie=actie_cli.__main__:main'],
    }
)
