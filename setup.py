from setuptools import setup, find_packages
from libs.actie import __name__, __version__


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name=__name__,
    version=__version__,
    description="A simple actor framework",
    long_description=readfile('README.md'),
    license=readfile('LICENSE'),
    author="Matteo Merz",
    author_email="matteo.merz@mail.polimi.it",
    url="https://github.com/mtt-merz/actie-cli",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['actie=cli.__main__:main'],
    }
)
