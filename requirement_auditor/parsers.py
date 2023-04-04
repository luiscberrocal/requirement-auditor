import re
from pathlib import Path
from typing import List, Dict, Any, Pattern

from .models import ParsedLine
from .settings import FULLY_PINNED_REGEX


def parse_line(line: str, line_number: int, regexp: Pattern = FULLY_PINNED_REGEX) -> ParsedLine:
    var_names = ['name', 'version', 'comment']
    match = regexp.match(line)
    requirement_line_dict = {'raw': line.replace('\n', ''), 'line_number': line_number, 'pinned': None}
    if match:
        requirement_line_dict['pinned'] = dict()
        for var_name in var_names:
            requirement_line_dict['pinned'][var_name] = match.group(var_name)  # type: ignore
    requirement_line = ParsedLine(**requirement_line_dict)
    return requirement_line


def parse_requirement_file(req_file: Path, regexp: Pattern = FULLY_PINNED_REGEX) -> List[ParsedLine]:
    with open(req_file, 'r') as r_file:
        lines = r_file.readlines()
    parsed_requirements = list()
    for i, line in enumerate(lines, 1):
        parsed_line = parse_line(line, i, regexp=regexp)
        parsed_requirements.append(parsed_line)
    return parsed_requirements
