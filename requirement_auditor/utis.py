import logging
import shutil
from datetime import datetime
from pathlib import Path

from requirement_auditor.exceptions import RequirementAuditorException

logger = logging.getLogger(__name__)

from . import __version__ as current_version


def backup_file(filename: Path, backup_folder: Path, add_version: bool = True) -> Path:
    if not backup_folder.is_dir():
        error_message = f'Backup folder has to be a folder.' \
                        f' Supplied: {backup_folder}. Type: {type(backup_folder)}'
        logger.error(error_message)
        raise RequirementAuditorException(error_message)

    datetime_format = '%Y%m%d_%H%M%S'
    try:
        if add_version:
            version_val = f'v{current_version}_'
        else:
            version_val = ''
        timestamp = datetime.now().strftime(datetime_format)
        backup_filename = backup_folder / f'{timestamp}_{version_val}{filename.name}'
        shutil.copy(filename, backup_filename)
        return backup_filename
    except Exception as e:
        error_message = f'Unexpected error backing up file {filename}. Type: {e.__class__.__name__}' \
                        f' error: {e}'
        logger.error(error_message)
        raise RequirementAuditorException(error_message)
