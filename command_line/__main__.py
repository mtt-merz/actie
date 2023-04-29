"""Actie entry point script."""
# actie/__main__.py

from command_line import __app_name__, command_line

def main():
    command_line.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
