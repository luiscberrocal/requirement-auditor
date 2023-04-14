import re
from pathlib import Path

from requirement_auditor import CONFIGURATION_MANAGER

STABLE_VERSION_REGEX = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.?(?P<patch>\d)?$")
FULLY_PINNED_REGEX = re.compile(r"^(?P<name>[\w_\-]+)==(?P<version>[\w.\-]+)\s*(?P<comment>#.*)?$")

try:
    CONFIGURATION = CONFIGURATION_MANAGER.get_configuration()
    LOG_FOLDER = CONFIGURATION['logs']['folder']
    LOG_FILE = Path(f'{LOG_FOLDER}/{CONFIGURATION["logs"]["filename"]}')
except KeyError:
    error_message = 'Error getting logs configuration. Check the configuration file.'
    LOG_FILE = CONFIGURATION_MANAGER.logs_folder / f'{CONFIGURATION_MANAGER.APP_NAME}.log'
    print(error_message)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(lineno)d  "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": str(LOG_FILE),
            "maxBytes": 1024,
            "backupCount": 3
        }
    },
    "loggers": {
        'requirement_auditor': {
            "level": "INFO",
            "handlers": ['console', 'file'],
            "propagate": False
        },
        'johnnydep': {
            "level": "INFO",
            "handlers": ['console', 'file'],
            "propagate": False
        },
    },
    "root": {"level": "INFO", "handlers": ["console", ]},
}
