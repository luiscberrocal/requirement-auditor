import os
from pathlib import Path

import pytest

from requirement_auditor.db import get_database, Project, Requirement


@pytest.fixture
def database():
    db_file = Path(__file__).parent / 'test_db.db'
    db = get_database(db_file)
    yield db
    os.remove(db_file)


def test_create_project(database):
    project = Project(name='cool-project')
    requirement_list = list()
    requirement_list.append(Requirement(name='Django', specs='==', version='3.2.9'))
    requirement_list.append(Requirement(name='django-test-tools', specs='==', version='2.0.0'))
    project.requirements = requirement_list
    database.add(project)
    database.commit()
    project_count = database.query(Project).count()
    assert project_count == 1
    assert database.query(Requirement).count() == 2
    assert database.query(Requirement).filter(Requirement.project == project).count() == 2
