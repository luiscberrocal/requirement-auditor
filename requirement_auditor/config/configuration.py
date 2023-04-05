import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

import toml

from .. import exceptions
from ..exceptions import ConfigurationError
from ..utis import backup_file


class ConfigurationManager:
    DEFAULT_CONFIG_FOLDER_NAME = '.requirement_auditor'
    DEFAULT_CONFIG_FILENAME = 'configuration.toml'
    APP_NAME = 'requirement-auditor'

    def __init__(self, home_folder: Optional[Path] = None,
                 config_filename: Optional[str] = None):
        if home_folder is None:
            self.config_folder = Path().home() / self.DEFAULT_CONFIG_FOLDER_NAME
        else:
            self.config_folder = home_folder / self.DEFAULT_CONFIG_FOLDER_NAME

        if config_filename is None:
            self.config_file = self.config_folder / self.DEFAULT_CONFIG_FILENAME
        else:
            self.config_file = self.config_folder / config_filename

        self.config_backup_folder = self.config_folder / 'backups'
        self.logs_folder = self.config_folder / 'logs'

        self.username = os.getlogin()
        self.prep_config()

    def get_sample_config(self) -> Dict[str, Any]:
        home = Path().home()
        data = {
            'application': {
                'database_folder': {
                    'folder': str(home / 'data'),
                    'prompt': 'Database folder'
                },
                'database_file':  {
                    'folder': str(home / 'data' / 'requirements_db.json'),
                    'prompt': 'Database file'
                },
                'timestamp_format': '%Y%m%d_%H%M%S'
            },
            'logs': {
                'folder': str(self.logs_folder),
                'filename': f'{self.APP_NAME}.log',
                'backup_count': 3
            },
        }
        return data

    def prep_config(self):
        self.config_folder.mkdir(exist_ok=True)
        self.config_backup_folder.mkdir(exist_ok=True)
        self.logs_folder.mkdir(exist_ok=True)
        if not self.config_file.exists():
            tmp_config = self.get_sample_config()
            self.write_configuration(tmp_config)

    def write_configuration(self, config_data: Dict[str, Any], overwrite: bool = False, ) -> None:
        if self.config_file.exists() and not overwrite:
            raise Exception('Cannot overwrite config file.')
        with open(self.config_file, 'w') as f:
            toml.dump(config_data, f)

    def get_configuration(self) -> Dict[str, Any]:
        if not self.config_folder.exists():
            error_message = 'No configuration file found. Run  config.'
            raise ConfigurationError(error_message)

        with open(self.config_file, 'r') as f:
            configuration = toml.load(f)
        return configuration

    def export_to_json(self, export_file: Path) -> None:
        config = self.get_configuration()
        with open(export_file, 'w') as f:
            json.dump(config, f)

    def backup(self) -> Path:
        backup_filename = backup_file(self.config_file, self.config_backup_folder)
        return backup_filename

    def delete(self) -> Path:
        backup_filename: Path = self.backup()
        self.config_file.unlink(missing_ok=True)
        return backup_filename

    @classmethod
    def get_current(cls):
        config = cls()
        return config.get_configuration()



