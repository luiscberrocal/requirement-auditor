"""
Update all
requirement-auditor database update

Update one requirement
requirement-auditor database update --name django

Add one requirement

requirement-auditor database add --name django

"""

import logging

import click

from requirement_auditor import DATABASE
from requirement_auditor.db.managers import update_single_requirement, update_requirements

logger = logging.getLogger(__name__)


@click.group()
def database():
    pass


@click.command(help='Database update database')
@click.option('-n', '--name')
def update(name: str | None = None) -> None:
    if name is None:
        logger.info('Started updating...')
        requirements_to_update = update_requirements(DATABASE)
        for req in requirements_to_update:
            db_req = DATABASE.get(req.name)
            msg = f'{req.name} latest_version {req.latest_version} > {db_req.latest_version} ' \
                  f'approved: {db_req.approved_version}'
            click.secho(msg, fg='green')
            update = click.prompt('Updated approved [y/n]?')
            if update.upper() == 'Y':
                DATABASE.update(req, fields=['approved_version', 'latest_version'])
            else:
                DATABASE.update(req, fields=['latest_version'])
            DATABASE.save()

    else:
        requirement = DATABASE.get(name)
        if requirement is None:
            click.secho(f'No requirement {name} found.', fg='yellow')
        req, updated = update_single_requirement(requirement)


database.add_command(update)
