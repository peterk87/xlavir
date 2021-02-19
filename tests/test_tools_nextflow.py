#!/usr/bin/env python

"""Tests for `xlavir.tools.nextflow` package."""

from pathlib import Path
from xlavir.tools.nextflow import exec_report

dirpath = Path(__file__).parent
input_html = dirpath / 'data/tools/nextflow/execution_report.html'

expected_report_info = {
    'workflow': 'nf-virontus',
    'execution_id': 'prickly_cuvier',
    'start_time': '17-Feb-2021 16:18:59',
    'completion_time': '17-Feb-2021 16:24:34',
    'command': 'nextflow run ../main.nf \\\n  --input samplesheet.csv \\\n  --genome false \\\n  --scov2 true \\\n  '
               '--freed \\\n  -resume \\\n  -profile docker \\\n  --tree_extra_fasta sequences.fasta \\\n  --tree '
               '\\\n  --outdir results',
    'project_directory': '/home/test/.nextflow/assets/peterk87/nf-virontus',
    'launch_directory': '/home/test/test',
    'workflow_profile': 'docker',
    'container': 'docker - peterk87/nf-virontus:2.0.0',
    'nextflow_version': 'version 20.10.0, build 5431 (01-11-2020 15:28 UTC)'
}


def test_parse_nextflow_exec_report_html():
    """Test finding and parsing of Nextflow workflow execution HTML report"""
    path = exec_report.find_exec_report(dirpath)
    assert str(path.absolute()) == str(input_html.absolute())
    info = exec_report.get_info(dirpath)
    assert isinstance(info, exec_report.NextflowWorkflowExecInfo)
    assert info.dict() == expected_report_info
