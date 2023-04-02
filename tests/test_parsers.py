from requirement_auditor.parsers import parse_line


def test_parse_line():
    raw_line = 'Sphinx==4.2.0  # https://github.com/sphinx-doc/sphinx'
    parsed = parse_line(raw_line, 1)
    assert parsed.raw == raw_line
    assert parsed.line_number == 1
