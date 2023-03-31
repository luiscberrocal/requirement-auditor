import configparser
import os
import shutil
from pathlib import Path
from unittest import mock

import pytest

from requirement_auditor._legacy.settings import write_configuration, get_user_configuration_file, create_default_config


@pytest.fixture
def configuration_folder():
    config_folder = Path(__file__).parent / '.requirement_auditor'
    if not os.path.exists(config_folder):
        os.mkdir(config_folder)
    yield config_folder
    if os.path.exists(config_folder):
        shutil.rmtree(config_folder)


@pytest.fixture
def configuration_file():
    out_file = Path(__file__).parent / 'test_config.cfg'
    yield out_file
    if os.path.exists(out_file):
        os.remove(out_file)


def test_write_configuration(configuration_file):
    config_data = dict()
    config_data['DEFAULT'] = {'folder': Path.home(),
                              'user': os.environ['USER']}
    config_data['cli'] = {'verbose': False}
    config = write_configuration(configuration_file, **config_data)
    config2 = configparser.ConfigParser()
    config2.read(configuration_file)
    assert config2 == config


@mock.patch('requirement_auditor.settings.Path.home')
def test_get_user_configuration_file(mock_home):
    mock_home.return_value = Path(__file__).parent
    filename, exists = get_user_configuration_file()
    assert not exists
    assert filename == Path(__file__).parent / '.requirement_auditor/config.cfg'


def test_create_default_config(configuration_folder):
    folder = Path(__file__).parent / '.requirement_auditor' / 'databases'
    config_data = create_default_config(configuration_folder)
    assert config_data['DEFAULT']['db_folder'] == folder
    assert os.path.exists(folder)
