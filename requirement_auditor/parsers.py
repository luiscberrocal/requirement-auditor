from pathlib import Path
import logging
from pathlib import Path
from typing import List, Pattern

from . import DATABASE
from .models import ParsedLine
from .settings import FULLY_PINNED_REGEX

logger = logging.getLogger(__name__)


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


def parse_and_update(req_file, regexp: Pattern = FULLY_PINNED_REGEX) -> int:
    parsed_lines = parse_requirement_file(req_file, regexp=regexp)
    updated = 0

    for parsed_line in parsed_lines:
        if parsed_line.pinned is not None:
            db_requirement = DATABASE.get(parsed_line.pinned.name)
            if db_requirement is not None:
                parsed_line.db_requirement = db_requirement
            else:
                logger.warning(f'Found requirement in file {req_file} not found in db.')
            print(parsed_line.pinned.name, parsed_line.pinned.version, parsed_line.db_requirement)
    with open(req_file, 'w') as rf:
        logger.info(f'Writing {req_file}')
        for parsed_line in parsed_lines:
            if parsed_line.pinned is None or parsed_line.db_requirement is None:
                rf.write(f'{parsed_line.raw}\n')
            else:
                comment = f'# {parsed_line.db_requirement.home_page}'
                rf.write(f'{parsed_line.db_requirement.name} == {parsed_line.db_requirement.approved_version} '
                         f'{comment}\n')
                updated += 1
    return updated
