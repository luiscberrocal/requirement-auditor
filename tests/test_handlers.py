from requirement_auditor.handlers import get_latest_version


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
    latest_version = get_latest_version('celery', stable_only=True)
    assert latest_version == '5.2.7'
    mock_get_versions.called_once()

