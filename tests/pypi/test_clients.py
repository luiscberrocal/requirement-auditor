import json
from pathlib import Path

from requirement_auditor.pypi.clients import SyncPyPiClient
from requirement_auditor.utils import convert_version_to_tuples


class TestSyncPyPiClient:

    def test_get_version(self):
        client = SyncPyPiClient()
        versions = client.get_versions('django')

        for i, version in enumerate(versions):
            print(i, version)

    def test_sort(self):
        versions = ['3.0.2', '1.1.14', '1.1.2', '1.2.21', '2.0.1']
        versions = sorted(versions)
        versions_tuples = []
        for i, v in enumerate(versions, 1):
            print(i, v)
            versions_tuples.append(convert_version_to_tuples(v))
        
        versions_tuples = sorted(versions_tuples)

        for i, v in enumerate(versions_tuples, 1):
            print(f'\t{i} {v}')
