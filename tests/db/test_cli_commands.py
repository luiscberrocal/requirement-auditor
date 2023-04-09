from click.testing import CliRunner

import requirement_auditor.db.cli_commands


def test_update_command():
    runner = CliRunner()
    result = runner.invoke(requirement_auditor.db.cli_commands.update)
    results = result.output.split('\n')
    assert result.exit_code == 0
    assert len(results) == 3
