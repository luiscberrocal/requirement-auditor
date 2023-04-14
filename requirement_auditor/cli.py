"""Console script for requirement_auditor."""
import sys
from pathlib import Path

import click

from requirement_auditor.config.cli_commands import config
from requirement_auditor.db.cli_commands import database
from requirement_auditor.parsers import parse_and_update
from . import __version__ as current_version


@click.group()
@click.version_option(version=current_version)
def main():
    pass


@click.command()
@click.option('-f', '--folder', type=click.Path(exists=True))
def parse(folder: Path):
    folder = Path(folder)
    files = ['local.txt', 'base.txt', 'production.txt', 'requirements.txt', 'requirements_dev.txt']
    for file in files:
        req_file = folder / file
        if req_file.exists():
            msg = f'Processing {file}'
            click.secho(msg, fg='green')
            parse_and_update(req_file)

main.add_command(database)
main.add_command(config)
main.add_command(parse)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
