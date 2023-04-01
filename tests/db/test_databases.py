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

    def test_update(self, json_db_file):
        db = JSONRequirementDatabase(json_db_file)
        requirement = PythonRequirement(name='my-package', latest_version='2.0.3',
                                        approved_version='2.0.0')
        db.create(requirement)
        db.save()
        requirement_to_update = PythonRequirement(name='my-package', latest_version='3.0.3',
                                                  approved_version='2.0.0', home_page='https://miuc.com/mmm')
        db.update(requirement_to_update)

        updated_requirement = db.get(requirement.name)

        assert requirement_to_update.approved_version == updated_requirement.approved_version
        assert requirement_to_update.approved_version_info == updated_requirement.approved_version_info
        assert requirement_to_update.construct == updated_requirement.construct
        assert requirement_to_update.copy == updated_requirement.copy
        assert requirement_to_update.dict == updated_requirement.dict
        assert requirement_to_update.environment == updated_requirement.environment
        assert requirement_to_update.group == updated_requirement.group
        assert requirement_to_update.home_page == updated_requirement.home_page
        assert requirement_to_update.json == updated_requirement.json
        assert requirement_to_update.last_updated == updated_requirement.last_updated
        assert requirement_to_update.latest_version == updated_requirement.latest_version
        assert requirement_to_update.latest_version_info == updated_requirement.latest_version_info
        assert requirement_to_update.license == updated_requirement.license
        assert requirement_to_update.name == updated_requirement.name
        assert requirement_to_update.parse_file == updated_requirement.parse_file
        assert requirement_to_update.parse_obj == updated_requirement.parse_obj
        assert requirement_to_update.parse_raw == updated_requirement.parse_raw
        assert requirement_to_update.schema == updated_requirement.schema
        assert requirement_to_update.schema_json == updated_requirement.schema_json
        assert requirement_to_update.to_req_line == updated_requirement.to_req_line
        assert requirement_to_update.update_forward_refs == updated_requirement.update_forward_refs

