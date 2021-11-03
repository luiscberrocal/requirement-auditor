import configparser
import os
from pathlib import Path

import pytest

from requirement_auditor.settings import write_configuration


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
