#!/usr/bin/env python

"""Tests for `xlavir` package."""
from pathlib import Path

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
