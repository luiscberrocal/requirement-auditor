import re
from typing import List, Union

from requirement_auditor.exceptions import RequirementAuditorException


class VersionRequirement:
    operator: str = '=='
    version: str = ''

    def __init__(self, operator, version):
        self.operator = operator
        self.version = version


class Comment:
    content: str = ''


class PythonRequirement:
    name: str = ''
    comment: str = ''
    line_number: int = -1
    REGEXP_REQUIREMENT = re.compile(
        r"(?P<library>[\w_-]+)(?P<specs>(?:[\>\<\=]=))(?P<version>[\w\.\-_]+)"
        r",?((?P<specs2>[><]=)(?P<version2>[\w\.\-_]+))?\s*(?:#(?P<comment>.*))?"
    )
    REGEXP_FILE = re.compile(r'^-r\s+(?P<file>[\w\-_\.\\\/]+txt)\s*#?(?P<comment>.*)?')

    def __init__(self, line: str):
        self.versions: List[VersionRequirement] = list()
        self.raw_line: str = line

    def __str__(self):
        if len(self.versions) == 1:
            return f'{self.name}{self.versions[0].operator}{self.versions[0].version}'
        elif len(self.versions) == 2:
            return f'{self.name}{self.versions[0].operator}{self.versions[0].version},' \
                   f'{self.versions[1].operator}{self.versions[1].version}'
        else:
            return f'# [RAW] {self.raw_line}'

    def add_version(self, operator, version):
        if len(self.versions) == 2:
            msg = 'You can only have up to 2 versions in a requirement.'
            raise RequirementAuditorException(msg)
        self.versions.append(VersionRequirement(operator, version))

    @classmethod
    def parse_line(cls, line: str) -> Union['PythonRequirement']:
        match = cls.REGEXP_REQUIREMENT.match(line)
        requirement = PythonRequirement(line)
        if match:
            requirement.name = match.group('library')
            if match.group('specs'):
                requirement.add_version(match.group('specs'), match.group('version'))
            if match.group('specs2'):
                requirement.add_version(match.group('specs2'), match.group('version2'))
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
