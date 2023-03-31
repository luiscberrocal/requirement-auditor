import configparser
import os
from pathlib import Path
from typing import Tuple, Dict, Any

DB_FILE = Path(__file__).parent / 'requirements_auditor.db'


def write_configuration(config_file: str, **kwargs: Dict[str, Any]) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    for key, item in kwargs.items():
        config[key] = item
    with open(config_file, 'w') as cfg_file:
        config.write(cfg_file)
    return config


def create_default_config(configuration_folder: Path) -> Dict[str, Any]:
    config_data = dict()
    db_folder = configuration_folder / 'databases'
    config_data['DEFAULT'] = {'db_folder': db_folder,
                              'db_filename': 'requirement_auditor.db'}
    if not os.path.exists(db_folder):
        os.mkdir(db_folder)
    return config_data


def get_or_create_configuration(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_user_configuration_file() -> Tuple['Path', bool]:
    home = Path.home()
    configuration_folder = home / '.requirement_auditor'
    if not os.path.exists(configuration_folder):
        os.mkdir(configuration_folder)
    config_file = configuration_folder / 'config.cfg'

    return config_file, os.path.exists(config_file)
