from pathlib import Path

from requirement_auditor.requirements.parsing import RequirementFile


def test_iter_requirement_file():
    filename = Path(__file__).parent / 'requirements_dev.txt'
    requirement_file = RequirementFile(filename)
    for req in requirement_file:
        print(f'>>>{req}')