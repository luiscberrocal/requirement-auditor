import os
import shutil
from pathlib import Path

import pytest

from requirement_auditor.db.databases import JSONRequirementDatabase


@pytest.fixture
def configuration_folder() -> Path:
    config_folder = Path(__file__).parent / '.requirement_auditor'
    config_folder.mkdir(exist_ok=True)
    yield config_folder
    if config_folder.exists():
        shutil.rmtree(config_folder)


@pytest.fixture
def configuration_file() -> Path:
    out_file = Path(__file__).parent / 'test_config.cfg'
    yield out_file
    if os.path.exists(out_file):
        os.remove(out_file)


@pytest.fixture(scope='session')
def output_folder() -> Path:
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def fixtures_folder() -> Path:
    folder = Path(__file__).parent / 'fixtures'
    return folder


@pytest.fixture()
def json_db_file(output_folder: Path) -> Path:
    file = output_folder / 'temp_db.json'
    yield file
    file.unlink(missing_ok=True)


@pytest.fixture()
def json_db(fixtures_folder) -> JSONRequirementDatabase:
    db_file = fixtures_folder / 'req_db_10_reqs.json'
    db = JSONRequirementDatabase(db_file, create_source=False)
    return db
