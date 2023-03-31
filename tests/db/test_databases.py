from requirement_auditor.db.databases import JSONRequirementDatabase
from requirement_auditor.models import PythonRequirement


class TestJSONRequirementDatabase:

    def test_blank_db(self, output_folder):
        db_file = output_folder / 'tmp.json'
        db_file.unlink()
        db = JSONRequirementDatabase(db_file)
        assert db.count() == 0

    def test_create_requirement(self, json_db_file):
        db = JSONRequirementDatabase(json_db_file)
        requirement = PythonRequirement(name='my-package', latest_version='2.0.3',
                                        approved_version='2.0.0')
        req = db.create(requirement)

        assert db.count() == 1
        assert req.last_updated is not None
        assert requirement.last_updated is not None

