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


if __name__ == '__main__':
    home = Path().home()
    db_file = Path(__file__).parent.parent / 'data' / 'req_db.json'
    db = JSONReqDatabase(db_file)
    output_folder = Path(__file__).parent.parent.parent.parent / 'output'
    # project = 'adelantos-cupos'
    # project = 'ec-d-local-payment-collector'
    # project = 'payment-queue-processor'
    # project = 'credibanco_integration'
    # project = 'movil-reseller-payments'
    # project = 'sms-integration'
    # project = 'payment_router'
    # project = 'multipagos-integrator'
    # project ='pj_django_payments/tests/example'
    # project = 'payment-collector'
    # project = 'bcp-integration'
    # project = 'stp_payment_provider'
    # project = 'adelantos-mail-sender'
    # project = 'puntopago_integration'
    project = 'wu-integration'
    command = 'CHANGE'
    if command == 'CHANGE':
        updater = Updater(db)
        files = ['local.txt', 'base.txt', 'production.txt', 'staging.txt']
        for file in files:
            f = home / f'adelantos/{project}/requirements/{file}'
            if f.exists():
                updater.update_requirements(f)
