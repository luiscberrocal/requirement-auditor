from typing import List


class PythonRequirement:
    name: str = ''
    specs: List[str] = list()
    version: str = ''
    comment: str = ':w'
    line_number: int = -1


class RequirementFile:

    def __init__(self, filename: str):
        self.filename = filename
        self.requirement_list: List[PythonRequirement] = list()

    def __iter__(self):
        with open(self.filename, 'r') as txt_file:
            for line in txt_file:
                yield line.strip()
