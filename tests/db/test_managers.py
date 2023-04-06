from requirement_auditor.db.managers import update_single_requirement


def test_update_single_requirement(mocker, json_db):
    latest_mocked_version = '5.0.5'
    mocker.patch('requirement_auditor.db.managers.get_latest_version', return_value=latest_mocked_version)
    requirement = json_db.get('django')
    assert requirement.latest_version == '4.1.4'

    new_requirement, updated = update_single_requirement(requirement, stable_only=True)

    assert updated
    assert new_requirement.latest_version == latest_mocked_version
    assert id(new_requirement) != id(requirement)
