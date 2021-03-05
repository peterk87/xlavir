from pathlib import Path
from typing import Optional

import pandas as pd

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
    for p in basedir.rglob('pangolin.lineage_report.csv'):
        return p


def read_pangolin_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.sort_values('taxon', inplace=True)

    df.rename(columns={x: y for x, y, _ in pangolin_cols}, inplace=True)
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
