import re
from pathlib import Path
from typing import Optional
import logging

import pandas as pd

from xlavir.util import find_file_for_each_sample

logger = logging.getLogger(__name__)

PANGOLIN_CSV = 'pangolin.lineage_report.csv'

PANGOLIN_GLOB_PATTERNS = [
    '**/*.pangolin.csv',
]

PANGOLIN_SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.pangolin\.csv$'),
]

pangolin_cols = [
    ('taxon', 'Sample', 'Sample name'),
    (
        'lineage',
        'Pangolin Lineage',
        'Pangolin global SARS-CoV-2 lineage assignment based on pangoLEARN model. '
        'For more info, see https://github.com/cov-lineages/pangolin/#pangolearn-description',
    ),
    (
        'probability',
        'Lineage Assignment Probability',
        'Pangolin lineage assignment probability from multinomial logistic regression. For more info, '
        'see https://github.com/cov-lineages/pangolin/#pangolearn-description'
    ),
    (
        'conflict',
        'Conflict',
        'This is a measure of conflicts within the decision tree, 0 being '
        'equivalent to no conflicts, but not a confidence score.'
    ),
    (
        'pangolin_version',
        'Pangolin Version',
        'Version of Pangolin (https://github.com/cov-lineages/pangolin) used for lineage assignment.'
    ),
    (
        'pango_version',
        'Pango Version',
        'pangoLEARN PANGO_VERSION (https://github.com/cov-lineages/pangoLEARN/)'
    ),
    (
        'pangoLEARN_version',
        'pangoLEARN Lineages Version',
        'Release version of pangoLEARN SARS-CoV-2 '
        'lineages information used for assignment.'),
    (
        'status',
        'Pangolin QC Status',
        'QC status of Pangolin lineage assignment, i.e. QC pass or fail'
    ),
    (
        'note',
        'Pangolin QC Note',
        'Issues reported with Pangolin lineage assignment such as too many Ns in the input sequence'
        ' (Pangolin will not call a lineage for sequences with over 50% (0.5) N-content) or '
        'if the sequence is too short (e.g. "seq_len:0")'
    ),
]


def find_pangolin_lineage_csv(basedir: Path) -> Optional[Path]:
    for p in basedir.rglob(PANGOLIN_CSV):
        return p


def read_pangolin_csv(path: Path, sample_name: str = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.sort_values('taxon', inplace=True)
    df.rename(columns={x: y for x, y, _ in pangolin_cols}, inplace=True)
    if sample_name:
        df['Sample'] = sample_name
    df.set_index('Sample', inplace=True)
    return df


def get_info(basedir: Path,
             pangolin_lineage_csv: Optional[Path] = None) -> Optional[pd.DataFrame]:
    if pangolin_lineage_csv:
        return read_pangolin_csv(pangolin_lineage_csv)
    else:
        path = find_pangolin_lineage_csv(basedir)
        if path:
            return read_pangolin_csv(path)
        else:
            logger.info(f'Could not find single Pangolin output CSV with filename "{PANGOLIN_CSV}". '
                        f'Searching for Pangolin output per sample with sample name in filename')
            pangolin_outputs = find_file_for_each_sample(basedir=basedir,
                                                         glob_patterns=PANGOLIN_GLOB_PATTERNS,
                                                         sample_name_cleanup=PANGOLIN_SAMPLE_NAME_CLEANUP)
            return pd.concat([read_pangolin_csv(p, s) for s, p in pangolin_outputs.items()])
