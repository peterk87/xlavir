import re
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup
import logging
from pydantic import BaseModel
from pathlib import Path

logger = logging.getLogger(__name__)


class NextflowWorkflowExecInfo(BaseModel):
    workflow: str
    execution_id: str
    start_time: str
    completion_time: str
    command: str
    project_directory: str
    launch_directory: str
    workflow_profile: str
    container: Optional[str] = None
    nextflow_version: str


def find_exec_report(basedir: Path) -> Path:
    for p in basedir.rglob('execution_report*.html'):
        return p


def parse(path: Path) -> NextflowWorkflowExecInfo:
    with open(path) as fh:
        soup = BeautifulSoup(fh, 'html.parser')
        execution_id = re.sub(r'\[(\w+)].*', r'\1', soup.find('head').find('title').text)
        command = soup.find(attrs={'class': 'nfcommand'}).text
        workflow_start = soup.find(id='workflow_start').text
        workflow_complete = soup.find(id='workflow_complete').text
        wf_attrs = soup.find(class_='container').find(class_='row').text.strip().split('\n')
        wf_attrs = {wf_attrs[i]: wf_attrs[i + 1] for i in range(0, len(wf_attrs), 2)}
        project_dir = wf_attrs.get('Project directory', 'UNKNOWN')
        if project_dir:
            workflow = Path(project_dir).name
        container_engine = wf_attrs.get('Container engine', None)
        wf_container = wf_attrs.get('Workflow container', None)
        container = None
        if wf_container and container_engine:
            container = f'{container_engine} - {wf_container}'
        nextflow_version = wf_attrs.get('Nextflow version', 'UNKNOWN')
        launch_directory = wf_attrs.get('Launch directory', 'UNKNOWN')
        workflow_profile = wf_attrs.get('Workflow profile', 'NA')

        return NextflowWorkflowExecInfo(workflow=workflow,
                                        execution_id=execution_id,
                                        start_time=workflow_start,
                                        completion_time=workflow_complete,
                                        command=command.replace(' -', ' \\\n  -'),
                                        container=container,
                                        nextflow_version=nextflow_version,
                                        project_directory=project_dir,
                                        launch_directory=launch_directory,
                                        workflow_profile=workflow_profile)


def get_info(basedir: Path) -> Optional[NextflowWorkflowExecInfo]:
    exec_report_path = find_exec_report(basedir)
    if exec_report_path:
        logger.info(f'Found Nextflow execution report')
        return parse(exec_report_path)
    else:
        logger.warning(f'Could not find Nextflow execution report in "{basedir}". '
                       f'Did you specify the input directory as a Nextflow output directory?')
        return None


def to_dataframe(nf_exec_info):
    df_exec_info = pd.DataFrame([(x, y) for x, y in nf_exec_info.dict().items()])
    df_exec_info.columns = ['Attribute', 'Value']
    df_exec_info.set_index('Attribute', inplace=True)
    return df_exec_info
