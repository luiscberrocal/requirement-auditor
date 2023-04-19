import json
from pathlib import Path

from requirement_auditor.pypi.clients import SyncPyPiClient


class TestSyncPyPiClient:

    def test_get_version(self):
        client = SyncPyPiClient()
        versions = client.get_versions('django')

        for i,version in enumerate(versions):
            print(i, version)
