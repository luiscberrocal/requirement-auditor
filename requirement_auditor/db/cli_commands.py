"""
Update all
requirement-auditor database update

Update one requirement
requirement-auditor database update --name django

Add one requirement

requirement-auditor database add --name django

"""
import click

@click.group()
def database():
    pass


@click.command(help='Database update database')
def update(name: str | None = None) -> None:
    pass


