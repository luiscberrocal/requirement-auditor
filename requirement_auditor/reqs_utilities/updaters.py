import logging
from pathlib import Path

from requirement_auditor.db.databases import JSONReqDatabase
from requirement_auditor.reqs_utilities.parsers import parse_requirement_file

logger = logging.getLogger(__name__)


class Updater:

    def __init__(self, database: JSONReqDatabase):
        self.database = database

    def update_requirements(self, requirement_file: Path):
        reqs = parse_requirement_file(requirement_file)
        lines = list()
        logger.debug(f'Ready to parse {len(reqs)} requirement.')
        for req in reqs:
            if req['parsed'] is None:
                lines.append(req['raw'])
            else:
                recommended = self.database.get(req['parsed']['lib_name'])
                if recommended is None:
                    lines.append(req['raw'])
                else:
                    line = recommended.to_req_line()
                    lines.append(f'{line}\n')

        with open(requirement_file, 'w') as r_file:
            string_lines = ''.join(lines)
            r_file.write(string_lines)
