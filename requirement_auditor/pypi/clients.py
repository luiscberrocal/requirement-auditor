from abc import ABC, abstractmethod
from typing import List

import httpx
import requests

from requirement_auditor.models import VersionNumber
from requirement_auditor.pypi.models import PyPiResponse


class PyPiClient(ABC):
    _base_url: str = 'https://pypi.org/pypi'

    @abstractmethod
    def get_versions(self, name: str):
        """Get versions from pypi website"""

    @abstractmethod
    def get_info(self, name: str, version: str) -> PyPiResponse:
        """Get PyPi Information"""


class SyncPyPiClient(PyPiClient):

    def get_versions(self, name: str):
        url = f'{self._base_url}/{name}/json'
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            releases = results.get('releases')
            if releases is None:
                return []
            t_versions = [VersionNumber.parse(x) for x in releases.keys()]
            # t_versions: List[VersionNumber] = []
            # for key in releases.keys():
            #     try:
            #         version: VersionNumber = VersionNumber.parse(key)
            #         if version is not None:
            #             t_versions.append(version)

            t_versions = sorted(t_versions)

            return t_versions

    def get_info(self, name: str, version: str) -> PyPiResponse:
        url = f'{self._base_url}/{name}/{version}/json'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pypi_response = PyPiResponse(**data)
            return pypi_response


class ASyncPyPiClient(PyPiClient):

    def get_versions(self, name: str):
        pass

    def get_info(self, name: str, version: str) -> PyPiResponse:
        url = f'{self._base_url}/{name}/{version}/json'
        response = httpx.get(url)
        if response.status_code == 200:
            data = response.json()
            pypi_response = PyPiResponse(**data)
            return pypi_response
