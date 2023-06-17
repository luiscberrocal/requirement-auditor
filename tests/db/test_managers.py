from requirement_auditor.db.managers import update_single_requirement, update_requirements


def test_update_single_requirement(mocker, json_db):
    latest_mocked_version = '5.0.5'
    mocker.patch('requirement_auditor.db.managers.get_latest_version', return_value=latest_mocked_version)
    requirement = json_db.get('django')
    assert requirement.latest_version == '4.1.4'

    new_requirement, updated = update_single_requirement(requirement, stable_only=True)

    assert updated
    assert new_requirement.latest_version == latest_mocked_version
    assert id(new_requirement) != id(requirement)


def test_update_requirements(mocker, json_db):
    def mock_get_latest_version(name: str, stable_only: bool):
        if name == 'django':
            return '5.2.0'
        else:
            req = json_db.get(name)
            return req.latest_version

    mocked_fun = mocker.patch('requirement_auditor.db.managers.get_latest_version', side_effect=mock_get_latest_version)
    updatable_requirements = update_requirements(json_db)
    assert mocked_fun.call_count == 10
    assert len(updatable_requirements) == 1
    assert updatable_requirements[0].name == 'django'


def test_print():
    for i in range(10):
        print('x', end='')
