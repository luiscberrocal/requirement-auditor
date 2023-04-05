"""Console script for requirement_auditor."""
import sys

import click

from . import __version__ as current_version


@click.group()
@click.version_option(version=current_version)
def main():
    pass

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
