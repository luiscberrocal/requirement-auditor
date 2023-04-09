from pydantic import BaseModel

from requirement_auditor.parsers import parse_line, parse_requirement_file


def test_parse_line():
    raw_line = 'Sphinx==4.2.0  # https://github.com/sphinx-doc/sphinx'
    parsed = parse_line(raw_line, 1)
    assert parsed.raw == raw_line
    assert parsed.line_number == 1


def test_parse_requirement_file(fixtures_folder):
    req_file = fixtures_folder / 'requirements_dev.txt'
    req_lines = parse_requirement_file(req_file)
    pinned_lines = [r for r in req_lines if r.pinned is not None]

    assert len(req_lines) == 21
    assert len(pinned_lines) == 14
    #for i, p in enumerate(pinned_lines, 1):
    #    print(f'{i} {p.raw}')

    assert req_lines[0].line_number == 1
    assert req_lines[0].raw == "-r ./base.txt"
    assert req_lines[0].pinned == None
    assert req_lines[0].db_requirement == None
    assert req_lines[1].line_number == 2
    assert req_lines[1].raw == ""
    assert req_lines[1].pinned == None
    assert req_lines[1].db_requirement == None
    assert req_lines[2].line_number == 3
    assert req_lines[2].raw == "Werkzeug==2.0.2 # pyup: < 0.15 # https://github.com/pallets/werkzeug"
    assert str(req_lines[2].pinned )== "name='Werkzeug' version='2.0.2' " \
                                       "comment='# pyup: < 0.15 # https://github.com/pallets/werkzeug'"
    assert req_lines[2].db_requirement == None
    assert req_lines[3].line_number == 4
    assert req_lines[3].raw == "ipdb==0.13.9  # https://github.com/gotcha/ipdb"
    assert str(req_lines[3].pinned) == "name='ipdb' version='0.13.9' comment='# https://github.com/gotcha/ipdb'"
    assert req_lines[3].db_requirement == None
    assert req_lines[4].line_number == 5
    assert req_lines[4].raw == "Sphinx==4.2.0  # https://github.com/sphinx-doc/sphinx"
    assert str(req_lines[4].pinned) == "name='Sphinx' version='4.2.0' comment='# https://github.com/sphinx-doc/sphinx'"
    assert req_lines[4].db_requirement == None
    assert req_lines[5].line_number == 6
    assert req_lines[5].raw == "psycopg2==2.8.6 --no-binary psycopg2  # https://github.com/psycopg/psycopg2"
    assert req_lines[5].pinned == None
    assert req_lines[5].db_requirement == None
    assert req_lines[6].line_number == 7
    assert req_lines[6].raw == "pip==21.3.1"
    assert str(req_lines[6].pinned) == "name='pip' version='21.3.1' comment=None"
    assert req_lines[6].db_requirement == None
    assert req_lines[7].line_number == 8
    assert req_lines[7].raw == "bump2version==1.0.1"
    assert str(req_lines[7].pinned) == "name='bump2version' version='1.0.1' comment=None"
    assert req_lines[7].db_requirement == None
    assert req_lines[8].line_number == 9
    assert req_lines[8].raw == "wheel==0.37.0"
    assert str(req_lines[8].pinned) == "name='wheel' version='0.37.0' comment=None"
    assert req_lines[8].db_requirement == None
    assert req_lines[9].line_number == 10
    assert req_lines[9].raw == "watchdog==2.1.6"
    assert str(req_lines[9].pinned) == "name='watchdog' version='2.1.6' comment=None"
    assert req_lines[9].db_requirement == None
    assert req_lines[10].line_number == 11
    assert req_lines[10].raw == "flake8==4.0.1# Blaa"
    assert str(req_lines[10].pinned) == "name='flake8' version='4.0.1' comment='# Blaa'"
    assert req_lines[10].db_requirement == None
    assert req_lines[11].line_number == 12
    assert req_lines[11].raw == "tox==3.24.4   # Comment"
    assert str(req_lines[11].pinned) == "name='tox' version='3.24.4' comment='# Comment'"
    assert req_lines[11].db_requirement == None
    assert req_lines[12].line_number == 13
    assert req_lines[12].raw == "coverage==6.1.1"
    assert str(req_lines[12].pinned) == "name='coverage' version='6.1.1' comment=None"
    assert req_lines[12].db_requirement == None
    assert req_lines[13].line_number == 14
    assert req_lines[13].raw == "Sphinx==4.2.0"
    assert str(req_lines[13].pinned) == "name='Sphinx' version='4.2.0' comment=None"
    assert req_lines[13].db_requirement == None
    assert req_lines[14].line_number == 15
    assert req_lines[14].raw == "twine==3.4.2"
    assert str(req_lines[14].pinned) == "name='twine' version='3.4.2' comment=None"
    assert req_lines[14].db_requirement == None
    assert req_lines[15].line_number == 16
    assert req_lines[15].raw == ""
    assert req_lines[15].pinned == None
    assert req_lines[15].db_requirement == None
    assert req_lines[16].line_number == 17
    assert req_lines[16].raw == "pytest==6.2.5"
    assert str(req_lines[16].pinned) == "name='pytest' version='6.2.5' comment=None"
    assert req_lines[16].db_requirement == None
    assert req_lines[17].line_number == 18
    assert req_lines[17].raw == "black==21.7b0"
    assert str(req_lines[17].pinned) == "name='black' version='21.7b0' comment=None"
    assert req_lines[17].db_requirement == None
    assert req_lines[18].line_number == 19
    assert req_lines[18].raw == "mypy>=0.910"
    assert req_lines[18].pinned == None
    assert req_lines[18].db_requirement == None
    assert req_lines[19].line_number == 20
    assert req_lines[19].raw == "Django>=2.0.0,<=3.0.0"
    assert req_lines[19].pinned == None
    assert req_lines[19].db_requirement == None
    assert req_lines[20].line_number == 21
    assert req_lines[20].raw == "django_test_tools>1.0.0"
    assert req_lines[20].pinned == None
    assert req_lines[20].db_requirement == None
