from datetime import datetime

from requirement_auditor.models import PythonRequirement


def test_is_behind():
    requirement = PythonRequirement(name='my-package', latest_version='2.0.3',
                                    approved_version='2.0.0', last_updated=datetime.now())
    is_behind = requirement.approved_version_info < requirement.latest_version_info
    assert is_behind
