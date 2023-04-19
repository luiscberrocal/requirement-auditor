from abc import ABC, abstractmethod

import requests

from requirement_auditor.pypi.models import PyPiResponse


class PyPiClient(ABC):
    _base_url: str = 'https://pypi.org/pypi/'

    @abstractmethod
    def get_versions(self, name: str):
        """Get versions from pypi website"""

    @abstractmethod
    def get_info(self, name: str, version: str) -> PyPiResponse:
        """Get PyPi Information"""


class SyncPyPiClient(PyPiClient):

    def get_versions(self, name: str):
        pass

    def get_info(self, name: str, version: str) -> PyPiResponse:
        url = f'{self._base_url}/{name}/{version}/json'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pypi_response = PyPiResponse(**data)
            return pypi_response
