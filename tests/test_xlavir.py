#!/usr/bin/env python

"""Tests for `xlavir` package."""
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from xlavir.cli import app

runner = CliRunner()

dirpath = Path(__file__).parent

test_image = dirpath / 'data/images/190px-Arthur-Pyle_Excalibur_the_Sword.JPG'


def test_command_line_interface():
    """Test the CLI."""
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert 'Error: Missing argument' in result.output
    help_result = runner.invoke(app, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
    with runner.isolated_filesystem():
        out_report = 'report.xlsx'
        result = runner.invoke(app, [str((dirpath / 'data').resolve().absolute()), out_report])
        if result.exception:
            raise result.exception
        assert result.exit_code == 0
        assert Path(out_report).exists()
        df = pd.read_excel(out_report)
        assert df.shape[0] == 3, 'First sheet in Excel report should have 3 entries'
