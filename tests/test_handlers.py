import pytest

from requirement_auditor.exceptions import LibraryNotFoundError
from requirement_auditor.handlers import get_latest_version, handle_pypi_info


def test_get_latest_version(mocker):
    response = ['5.2.6', '5.2.7', '5.3.0a1', '5.3.0b1', '5.3.0b2']
    mock_get_versions = mocker.patch('requirement_auditor.handlers.get_versions', return_value=response)
    latest_version = get_latest_version('celery', stable_only=False)
    assert latest_version == '5.3.0b2'
    mock_get_versions.called_once()


def test_get_latest_version_stable_only(mocker):
    response = ['5.2.6', '5.2.7', '5.3.0a1', '5.3.0b1', '5.3.0b2']
    mock_get_versions = mocker.patch('requirement_auditor.handlers.get_versions', return_value=response)
    latest_version = get_latest_version('celery', stable_only=True)
    assert latest_version == '5.2.7'
    mock_get_versions.called_once()


def test_get_latest_version_no_stable(mocker):
    response = ['5.3.0a1', '5.3.0b1', '5.3.0b2']
    mock_get_versions = mocker.patch('requirement_auditor.handlers.get_versions', return_value=response)
    name = 'celery'
    with pytest.raises(LibraryNotFoundError) as e:
        get_latest_version(name, stable_only=True)

    assert str(e.value) == f'Could not find stable version for {name} library.'
    mock_get_versions.called_once()


def test_get_latest_version_nonexistent_lib(mocker):
    response = []
    mock_get_versions = mocker.patch('requirement_auditor.handlers.get_versions', return_value=response)
    name = 'celery-dewr'
    with pytest.raises(LibraryNotFoundError) as e:
        get_latest_version(name, stable_only=True)

    assert str(e.value) == f'Library {name} not found.'
    mock_get_versions.called_once()


def test_handle_pypi_info():
    name = 'django'
    version = '3.2.18'
    info = handle_pypi_info(name, version)
    info_dict = info.dict()
    print(info)
    pytest.fail("Not implemented yet")


def test_handle_pypi_info_db(json_db_full_size):
    requirement_list = json_db_full_size.filter()
    for i, req in enumerate(requirement_list):
        try:
            info = handle_pypi_info(req.name, req.approved_version)
        except Exception as e:
            print(f'{i} req {req.name} {req.approved_version}')
            raise e
