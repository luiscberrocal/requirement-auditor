import click

from requirement_auditor import CONFIGURATION_MANAGER


@click.command()
def config():
    if CONFIGURATION_MANAGER.config_file.exists():
        sample_config = CONFIGURATION_MANAGER.get_sample_config()
        CONFIGURATION_MANAGER.write_configuration(sample_config)
        msg = f'Wrote configuration to {CONFIGURATION_MANAGER.config_file}'
        click.secho(msg, fg='green')
