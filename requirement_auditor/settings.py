import configparser
import os
from pathlib import Path

DB_FILE = Path(__file__).parent / 'requirements_auditor.db'


def write_configuration(config_file, **kwargs):
    config = configparser.ConfigParser()
    for key, item in kwargs.items():
        config[key] = item
    with open(config_file, 'w') as cfg_file:
        config.write(cfg_file)
    return config


def get_or_create_configuration(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_user_configuration_file():
    home = Path.home()
    configuration_folder = home / '.gitlab_ci_tools_2'
    if not os.path.exists(configuration_folder):
        os.mkdir(configuration_folder)
        print(f'Created {configuration_folder}')
    config_file = configuration_folder / 'config.cfg'

    return config_file, os.path.exists(config_file)
