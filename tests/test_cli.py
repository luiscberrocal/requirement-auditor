from click.testing import CliRunner

from requirement_auditor.cli import parse


def test_update_command(fixtures_folder):
    req_file = fixtures_folder
    runner = CliRunner()
    result = runner.invoke(parse, ['-d', fixtures_folder])
    results = result.output.split('\n')

    assert result.exit_code == 0
    assert len(results) == 3
