import re
from typing import List, Union


class VersionRequirement:
    operator: str = '=='
    version_number: str = ''


class PythonRequirement:
    name: str = ''
    versions: List[VersionRequirement] = list()
    comment: str = ''
    line_number: int = -1
    regexp_req_with_comment = re.compile(
        r"(?P<library>[\w_-]+)(?P<specs>(?:[\>\<\=]=))(?P<version>[\w\.\-_]+)"
        r",?((?P<specs2>[><]=)(?P<version2>[\w\.\-_]+))?\s*(?:#(?P<comment>.*))?"
    )

    def __str__(self):
        if len(self.versions) == 1:
            return f'{self.name}{self.versions[0].operator}{self.versions[0].version_number}'
        else:
            return f'{self.name}{self.versions[0].operator}{self.versions[0].version_number},' \
                   f'{self.versions[1].operator}{self.versions[1].version_number}'

    @classmethod
    def parse_line(cls, line: str) -> Union['PythonRequirement', None]:
        match = cls.regexp_req_with_comment.match(line)
        requirement = None
        if match:
            requirement = PythonRequirement()
            requirement.name = match.group('library')
            if match.group('specs'):
                version = VersionRequirement()
                version.operator = match.group('specs')
                version.version_number = match.group('version')
                requirement.versions.append(version)

            if match.group('specs2'):
                version = VersionRequirement()
                version.operator = match.group('specs2')
                version.version_number = match.group('version2')
                requirement.versions.append(version)

            requirement.comment = match.group('comment')
        return requirement


class RequirementFile:

    def __init__(self, filename: str):
        self.filename = filename
        self.requirement_list: Union[List[PythonRequirement], None] = None

    @property
    def requirements(self):
        if self.requirement_list is None:
            self.requirement_list = list(self)
        return self.requirement_list

    def __iter__(self):
        if isinstance(self.requirement_list, list):
            for req in self.requirement_list:
                yield req
            return

        with open(self.filename, 'r') as txt_file:
            for line in txt_file:
                requirement = PythonRequirement.parse_line(line.strip())
                yield requirement
