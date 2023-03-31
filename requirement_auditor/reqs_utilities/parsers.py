import json
import re
from pathlib import Path
from typing import Dict, Any, List

from requirement_auditor.reqs_utilities.database import RequirementDatabase


# def parse_for_permitted_libs(req_file: Path):
#     regexp = re.compile(r'(?P<lib_name>[\w_\-]+)==(?P<version>[\w\.\-]+)\s*#?(?P<comment>.*)')
#     with open(req_file, 'r') as r_file:
#         lines = r_file.readlines()
#     parsed_requirements = dict()
#     for i, line in enumerate(lines, 1):
#         match = regexp.match(line)
#         if match:
#             lib_name = match.group('lib_name')
#             parsed_requirements[lib_name] = match.group('version')
#     return parsed_requirements


def parse_requirement_file(req_file: Path) -> List[Dict[str, Any]]:
    regexp = re.compile(r'(?P<lib_name>[\w_\-]+)==(?P<version>[\w\.\-]+)\s*#?(?P<comment>.*)')
    with open(req_file, 'r') as r_file:
        lines = r_file.readlines()
    var_names = ['lib_name', 'version', 'comment']
    parsed_requirements = list()
    for i, line in enumerate(lines, 1):
        match = regexp.match(line)
        req = {'raw': line, 'line_number': i, 'parsed': None}
        if match:
            req['parsed'] = dict()
            for var_name in var_names:
                req['parsed'][var_name] = match.group(var_name)
        parsed_requirements.append(req)
    return parsed_requirements


def interactive_parse_requirements(req_file: Path, db: RequirementDatabase):
    requirements = parse_requirement_file(req_file)
    for requirement in requirements:
        if requirement.get('parsed'):
            name = requirement['parsed']['lib_name']
            version = requirement['parsed']['version']
            db_requirement = db.get(name)
            if db_requirement is not None:
                version_info = convert_version_to_tuples(version)
                if version_info <= db_requirement.approved_version_info:
                    print(f"{name} - {version}  {db_requirement.latest_version} {db_requirement.approved_version}")
            else:
                add_to_db = input(f'Add {name} version {version} to db?')
                if add_to_db.upper() == 'Y':
                    db.add(name, None)


def save_requirements_to_json(filename: Path, folder: Path):
    out_file = folder / 'reqs.json'
    reqs = parse_requirement_file(filename)

    with open(out_file, 'w') as d_file:
        json.dump(reqs, d_file)


def main2(requirements_folder: Path, folder: Path):
    out_file = folder / 'permitted.json'
    req_files = requirements_folder.glob('**/*.txt')
    global_req = dict()
    for req_file in req_files:
        reqs = parse_for_permitted_libs(req_file)
        global_req.update(reqs)
    with open(out_file, 'w') as d_file:
        json.dump(global_req, d_file)


if __name__ == '__main__':
    home = Path().home()
    # db_file = home / 'PycharmProjects/django_scaffolding_tools/tests/fixtures/_experimental/req_db.json'
    db_file = Path(__file__).parent / 'req_db.json'
    if not db_file.exists():
        raise Exception('File not found')
    db = RequirementDatabase(db_file)

    project = 'adelantos-cupos'
    project = 'ec-d-local-payment-collector'
    # project = 'payment-queue-processor'
    # project = 'credibanco_integration'
    # project = 'movil-reseller-payments'
    # project = 'sms-integration'
    # project = 'payment_router'
    command = 'UPDATE'
    files = ['local.txt', 'base.txt', 'production.txt']
    for file in files:
        f = home / f'adelantos/{project}/requirements/{file}'
        interactive_parse_requirements(f, db)
