"""
Update all
requirement-auditor database update

Update one requirement
requirement-auditor database update --name django

Add one requirement

requirement-auditor database add --name django

"""
from pprint import pprint

import click

from requirement_auditor import CONFIGURATION_MANAGER, DATABASE
from requirement_auditor.db.managers import update_single_requirement, update_requirements


@click.group()
def database():
    pass


@click.command(help='Database update database')
@click.option('-n', '--name')
def update(name: str | None = None) -> None:
    print('Update database')
    if name is None:
        requirement = DATABASE.get(name)
        if requirement is None:
            click.secho(f'No requirement {name} found.', fg='yellow')
        req, updated = update_single_requirement(requirement)
    else:
        requirements_to_update = update_requirements(DATABASE)
        for req in requirements_to_update:
            msg = f'{req.name}'
            click.secho(msg, fg='green')


database.add_command(update)
