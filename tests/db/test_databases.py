import json

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

    def test_save(self, json_db_file):
        db = JSONRequirementDatabase(json_db_file)
        requirement = PythonRequirement(name='my-package', latest_version='2.0.3',
                                        approved_version='2.0.0')
        db.create(requirement)
        db.save()

        with open(json_db_file, 'r') as j_file:
            db_dict = json.load(j_file)

        assert db_dict['my-package']['name'] == requirement.name
        assert db_dict['my-package']['latest_version'] == requirement.latest_version
        assert db_dict['my-package']['approved_version'] == requirement.approved_version
        assert db_dict['my-package']['group'] == requirement.group
        assert db_dict['my-package']['environment'] == requirement.environment
        assert db_dict['my-package']['last_updated'] == str(requirement.last_updated)
        assert db_dict['my-package']['home_page'] == requirement.home_page
        assert db_dict['my-package']['license'] == requirement.license

