"""
Update all
requirement-auditor database update

Update one requirement
requirement-auditor database update --name django

Add one requirement

requirement-auditor database add --name django

"""

import logging
from pathlib import Path

import click

from requirement_auditor import DATABASE
from requirement_auditor.db.managers import update_single_requirement, update_requirements
from requirement_auditor.handlers import get_latest_version, handle_pypi_info
from requirement_auditor.models import PythonRequirement
from requirement_auditor.pypi.models import PyPiResponse
from requirement_auditor.reqs_utilities.updaters import Updater

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
            should_update = click.prompt('Updated approved [y/n]?')
            if should_update.upper() == 'Y':
                req.approved_version = req.latest_version
                DATABASE.update(req)  # , fields=['approved_version', 'latest_version'])
            else:
                pass
                # DATABASE.update(req, fields=['latest_version'])
            DATABASE.save()

    else:
        requirement = DATABASE.get(name)
        if requirement is None:
            click.secho(f'No requirement {name} found.', fg='yellow')
        req, updated = update_single_requirement(requirement)


@click.command()
@click.option('-n', '--name')
def add(name: str):
    req = DATABASE.get(name)
    if req is not None:
        click.secho(f'Requirement {name}already exists', fg='red')
        return None
    version = get_latest_version(name, stable_only=True)
    click.secho(f'Lib {name} {version}')
    pypi_info: PyPiResponse = handle_pypi_info(name, version)
    click.secho(f'Licence {pypi_info.info.license}', fg='green')
    click.secho(f'Home {pypi_info.info.home_page}', fg='green')
    req = PythonRequirement(name=name, approved_version=version,
                            latest_version=version,
                            home_page=pypi_info.info.home_page or None,
                            license=pypi_info.info.license or None)
    prompt = click.prompt('Add?')
    if prompt.upper() == 'Y':
        DATABASE.create(req)
        DATABASE.save()


@click.command(help='Database update database')
@click.option('project_folder', '-d', '--directory', type=click.Path(exists=True))
@click.option('-n', '--name')
def upgrade(project_folder: Path, name: str):
    project_folder = Path(project_folder)
    matching_folders = []
    for folder in project_folder.iterdir():
        if name in folder.name:
            matching_folders.append(folder)
    for i, folder in enumerate(matching_folders):
        click.secho(f'[{i}] {folder.name}', fg='green')
    index = click.prompt(f'Select folder', type=int)
    folder_to_update = matching_folders[index]
    print(f'{folder_to_update=}')
    updater = Updater(DATABASE)
    files = ['local.txt', 'base.txt', 'production.txt', 'staging.txt']
    for file in files:
        f = folder_to_update / f'requirements/{file}'
        print(f'{f=}')
        if f.exists():
            updater.update_requirements(f)
            click.secho(f'Upgraded f{f}')


database.add_command(upgrade)
database.add_command(update)
database.add_command(add)
