#!/usr/bin/env python

"""Tests for `xlavir.tools.nextflow` package."""

from pathlib import Path

from xlavir.tools import fastp

dirpath = Path(__file__).parent

expected = {
    'Sample1': 133769420,
    'Sample2': 523300,
}


def test_fastp_get_total_reads():
    """Test finding and parsing of Nextflow workflow execution HTML report"""
    sample_reads = fastp.get_info(dirpath)
    assert sample_reads == expected
