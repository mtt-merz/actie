from actie import __app_name__
from command_line import command_line


def main():
    command_line.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
