import re
from re import Pattern

import requests
from johnnydep.pipper import get_versions

from .exceptions import LibraryNotFoundError
from .pypi.models import PyPiResponse
from .settings import STABLE_VERSION_REGEX


def is_stable_version(version: str, regexp: Pattern = STABLE_VERSION_REGEX) -> bool:
    match = regexp.match(version)
    return match is not None


def get_latest_version(name: str, stable_only: bool) -> str:
    versions = get_versions(name)
    if len(versions) == 0:
        raise LibraryNotFoundError(f'Library {name} not found.')
    if stable_only:
        position = -1
        while True:
            try:
                latest_version = versions[position]
                if is_stable_version(latest_version):
                    return latest_version
                position -= 1
            except IndexError:
                raise LibraryNotFoundError(f'Could not find stable version for {name} library.')
    else:
        latest_version = versions[-1]
    return latest_version


def handle_pypi_info(name: str, version: str) -> PyPiResponse:
    url = f'https://pypi.org/pypi/{name}/{version}/json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pypi_response = PyPiResponse(**data)
        # import json
        # from pathlib import Path
        # var_name = 'data'
        # data = eval(var_name)
        # filename = Path(__file__).parent.parent / 'output' / f'_{var_name}.json'
        # with open(filename, 'w') as json_file:
        #     json.dump(data, json_file, indent=4)
        return pypi_response
