from datetime import datetime

from requirement_auditor.models import PythonRequirement, VersionNumber


def test_is_behind():
    requirement = PythonRequirement(name='my-package', latest_version='2.0.3',
                                    approved_version='2.0.0', last_updated=datetime.now())
    is_behind = requirement.approved_version_info < requirement.latest_version_info
    assert is_behind


class TestVersionNumber:

    def test_greater_than(self):
        req1 = VersionNumber(major=2, minor=1, patch=1)
        req2 = VersionNumber(major=2, minor=1, patch=12)

        assert req2 > req1

    def test_greater_than2(self):
        version_low = VersionNumber(major=2, minor=1, patch=1)
        version_high = VersionNumber(major=3, minor=1, patch='b-0')

        assert version_low < version_high
        assert version_high > version_low

    def test_greater_than3(self):
        version_low = VersionNumber(major=3, minor=1, patch='rc1')
        version_high = VersionNumber(major=3, minor=1, patch='rc2')

        assert version_high > version_low

    def test_parse(self):
        version_high = VersionNumber.parse('2.1.33')
        version_low = VersionNumber.parse('2.1.3')

        assert version_high > version_low
        assert version_low < version_high
