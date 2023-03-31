import json
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

import requests
from johnnydep.pipper import get_versions
from pydantic import ValidationError

from requirement_auditor.models import RecommendedRequirement


class RequirementDatabase(ABC):

    @abstractmethod
    def create(self):
        """Create a new requirement in the database"""

    @abstractmethod
    def get(self):
        """Get a requirement by name"""

    @abstractmethod
    def update(self):
        """Updates a requirement"""

    @abstractmethod
    def delete(self):
        """Delete a requirment by name"""

    @abstractmethod
    def save(self):
        """Saves all changes to the file"""


class JSONRequirementDatabase:

    def __init__(self, source_file: Path):
        self.source_file = source_file
        self.regexp = re.compile(r'(?P<lib_name>[\w_\-]+)==(?P<version>[\w\.\-]+)\s*#?(?P<comment>.*)')
        self.database = dict()
        self.load_db(self.source_file)

    def load_db(self, source_file: Path):
        with open(source_file, 'r') as j_file:
            data = json.load(j_file)
        for name, req_dict in data.items():
            try:
                self.database[name] = RecommendedRequirement(**req_dict)
            except ValidationError as e:
                error_message = f'Invalid {name} library content. {e}'
                raise Exception(error_message)

    def get(self, name: str) -> RecommendedRequirement:
        return self.database.get(name)

    def add(self, name: str, environment: Optional[str], version: Optional[str] = None,
            commit: bool = True) -> RecommendedRequirement:
        if self.get(name) is not None:
            raise Exception(f'Library {name} already exists use update.')
        versions = get_versions(name)
        if len(versions) == 0:
            raise Exception(f'Library {name} not found')
        latest_version = versions[-1]
        approved_version = version if version is not None else latest_version
        recommended = RecommendedRequirement(name=name, latest_version=latest_version,
                                             approved_version=approved_version,
                                             environment=environment)
        info = self._download_info(name, recommended.approved_version)
        recommended.home_page = info['home_page']
        recommended.license = info['license']
        recommended.last_updated = datetime.now()
        self.database[name] = recommended
        if commit:
            self.save()
        return recommended

    def update(self, name: str) -> RecommendedRequirement:
        req = self.get(name)
        if req is None:
            raise Exception(f'Requirement {name} does not exist.')
        versions = get_versions(name)
        if len(versions) == 0:
            raise Exception(f'Library {name} not found')
        latest_version = versions[-1]
        req.approved_version = latest_version
        req.latest_version = latest_version
        req.last_updated = datetime.now()
        self.database[name] = req
        self.save()
        return req

    def update_db(self, commit: bool = True):
        for name, req in self.database.items():
            info = self._download_info(name, req.approved_version)
            req.home_page = info['home_page']
            req.license = info['license']
            req.last_updated = datetime.now()
        if commit:
            self.save()

    def _download_info(self, name: str, version: str):
        url = f'https://pypi.org/pypi/{name}/{version}/json'
        response = requests.get(url)
        info = dict()
        if response.status_code == 200:
            data = response.json()
            home_page = data['info']['home_page']
            lic = data['info']['license']
            info = {'home_page': home_page, 'license': lic}
        return info

    def save(self):
        tmp = dict()
        for name, req in self.database.items():
            tmp[name] = req.dict()
        with open(self.source_file, 'w') as f:
            json.dump(tmp, f, indent=4, default=str)

    def get_from_requirements_folder(self, folder: Path):
        req_files = folder.glob('**/*.txt')
        global_req = dict()
        for req_file in req_files:
            reqs = self.get_from_requirement_file(req_file)
            global_req.update(reqs)
        return global_req

    def get_from_requirement_file(self, req_file: Path) -> Dict[str, RecommendedRequirement]:
        with open(req_file, 'r') as r_file:
            lines = r_file.readlines()
        parsed_requirements = dict()
        for i, line in enumerate(lines, 1):
            match = self.regexp.match(line)
            if match:
                lib_name = match.group('lib_name')
                versions = get_versions(lib_name)
                if len(versions) == 0:
                    raise Exception(f'Library {lib_name} not found')
                latest_version = versions[-1]
                recommended = RecommendedRequirement(name=lib_name, latest_version=latest_version,
                                                     approved_version=match.group('version'),
                                                     environment=req_file.stem)
                parsed_requirements[lib_name] = recommended
        return parsed_requirements


def check_for_new_requirements(db: JSONRequirementDatabase):
    for name, req in db.database.items():
        info = db._download_info(name, req.approved_version)
        versions = get_versions(name)
        latest = versions[-1]
        if latest == req.approved_version:
            continue
        print(f'{name} {latest}')
        print(f'Approved {req.approved_version} Latest{req.latest_version}')
        print(info)
        action = input('Update approved?')
        if action.upper() == 'Y':
            req.approved_version = latest
            req.latest_version = latest
            req.last_updated = datetime.now()
            db.save()


if __name__ == '__main__':
    db_file = Path(__file__).parent / 'req_db.json'
    db = JSONRequirementDatabase(db_file)
    check_for_new_requirements(db)
