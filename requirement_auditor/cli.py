"""Console script for requirement_auditor."""
import sys

import click

from requirement_auditor.config.cli_commands import config
from requirement_auditor.db.cli_commands import database
from . import __version__ as current_version


@click.group()
@click.version_option(version=current_version)
def main():
    pass


main.add_command(database)
main.add_command(config)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
