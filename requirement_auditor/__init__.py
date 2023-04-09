"""Top-level package for Requirement Auditor."""

__author__ = """Luis C. Berrocal"""
__email__ = 'luis.berrocal.1942@gmail.com'
__version__ = '2.0.0'

from pathlib import Path

from requirement_auditor.config.configuration import ConfigurationManager
from requirement_auditor.db.databases import JSONRequirementDatabase


def logger_configuration():
    import logging.config
    from requirement_auditor.settings import LOGGING
    logging.config.dictConfig(LOGGING)



CONFIGURATION_MANAGER = ConfigurationManager()
db_file = Path(CONFIGURATION_MANAGER.get_current()['application']['database_file']['file'])
DATABASE = JSONRequirementDatabase(db_file)


logger_configuration()

del db_file
