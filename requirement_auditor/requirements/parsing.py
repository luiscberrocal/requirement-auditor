import re
from typing import List, Union


class PythonRequirement:
    name: str = ''
    specs: List[str] = list()
    version: str = ''
    comment: str = ''
    line_number: int = -1
    regexp_req_with_comment = re.compile(
        r"(?P<library>[\w_-]+)(?P<specs>(?:[\>\<\=]=))(?P<version>[\w\.\-_]+)"
        r",?((?P<specs2>[><]=)(?P<version2>[\w\.\-_]+))?\s*(?:#(?P<comment>.*))?"
    )
    def __str__(self):
        return f'{self.name} {self.version}'

    @classmethod
    def parse_line(cls, line: str) -> Union['PythonRequirement', None]:
        match = cls.regexp_req_with_comment.match(line)
        requirement = None
        if match:
            requirement = PythonRequirement()
            requirement.name = match.group('library')
            requirement.specs.append(match.group('specs'))
            requirement.version = match.group('version')
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
