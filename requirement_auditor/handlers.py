import re
from re import Pattern

from johnnydep.pipper import get_versions

from .exceptions import LibraryNotFoundError
from .settings import STABLE_VERSION_REGEX


def is_stable_version(version: str, regexp: Pattern = STABLE_VERSION_REGEX) -> bool:
    match = regexp.match(version)
    return match is not None


def get_latest_version(name: str, stable_only: bool) -> str:
    versions = get_versions(name)
    if len(versions) == 0:
        raise LibraryNotFoundError(f'Library {name} not found')
    if stable_only:
        position = -1
        while True:
            latest_version = versions[position]
            if is_stable_version(latest_version):
                return latest_version
            position -= 1
    else:
        latest_version = versions[-1]
    return latest_version
