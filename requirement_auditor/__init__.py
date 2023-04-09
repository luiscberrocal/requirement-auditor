"""Top-level package for Requirement Auditor."""

__author__ = """Luis C. Berrocal"""
__email__ = 'luis.berrocal.1942@gmail.com'
__version__ = '2.0.0'

from pathlib import Path

from requirement_auditor.config.configuration import ConfigurationManager
from requirement_auditor.db.databases import JSONRequirementDatabase

CONFIGURATION_MANAGER = ConfigurationManager()
db_file = Path(CONFIGURATION_MANAGER.get_current()['application']['database_file']['file'])
DATABASE = JSONRequirementDatabase(db_file)

del db_file
