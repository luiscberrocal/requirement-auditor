import json
from datetime import datetime

from freezegun import freeze_time

from requirement_auditor.db.databases import JSONRequirementDatabase
from requirement_auditor.models import PythonRequirement


class TestJSONRequirementDatabase:

    def test_blank_db(self, output_folder):
        db_file = output_folder / 'tmp.json'
        db_file.unlink()
        db = JSONRequirementDatabase(db_file)
        assert db.count() == 0

    @freeze_time('2023-02-03 16:40:00')
    def test_create_requirement(self, json_db_file):
        update_date = datetime(2023, 2, 3, 16, 40, 0)
        db = JSONRequirementDatabase(json_db_file)
        requirement = PythonRequirement(name='my-package', latest_version='2.0.3',
                                        approved_version='2.0.0')
        req = db.create(requirement)

        assert db.count() == 1
        assert req.last_updated == update_date
        assert requirement.last_updated == update_date

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

    @freeze_time('2023-02-03 16:40:00')
    def test_update(self, json_db_file):
        update_date = datetime(2023, 2, 3, 16, 40, 0)
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
        assert requirement_to_update.dict == updated_requirement.dict
        assert requirement_to_update.environment == updated_requirement.environment
        assert requirement_to_update.group == updated_requirement.group
        assert requirement_to_update.home_page == updated_requirement.home_page
        assert requirement_to_update.json == updated_requirement.json

        assert requirement_to_update.last_updated == update_date

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

    def test_delete(self, json_db):
        assert json_db.count() == 10

        json_db.delete('celery')

        assert json_db.count() == 9
        assert json_db.get('celery') is None
