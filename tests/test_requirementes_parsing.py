from pathlib import Path

from requirement_auditor.requirements.parsing import RequirementFile, PythonRequirement


def test_iter_requirement_file():
    filename = Path(__file__).parent / 'fixtures/requirements_dev.txt'
    requirement_file = RequirementFile(filename)
    assert len(requirement_file.requirements) == 13
    assert requirement_file.requirements[0].name == 'pip'
    assert requirement_file.requirements[0].versions[0].operator == '=='
    assert requirement_file.requirements[0].versions[0].version == '21.3.1'


def test_iteration():
    filename = Path(__file__).parent / 'fixtures/requirements_dev.txt'
    requirement_file = RequirementFile(filename)
    for req in requirement_file.requirements:
        print(f'>>>{req}')


def test_python_requirement_regexp():
    reqs = ['Pip==3.4.5']
    for req in reqs:
        match = PythonRequirement.regexp_req_with_comment.match(req)
        print(match)


def test_parse_line():
    reqs = ['Pip==3.4.5']
    for req in reqs:
        requirement = PythonRequirement.parse_line(req)
        print(requirement)
