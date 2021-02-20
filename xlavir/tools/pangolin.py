from pathlib import Path
from typing import Optional

import pandas as pd


def find_pangolin_lineage_csv(basedir: Path) -> Optional[Path]:
    for p in basedir.rglob('pangolin.lineage_report.csv'):
        return p


def read_pangolin_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.sort_values('taxon', inplace=True)
    pangolin_cols = [
        ('taxon', 'Sample'),
        ('lineage', 'Pangolin Lineage'),
        ('probability', 'Lineage Assignment Probability'),
        ('pangoLEARN_version', 'pangoLEARN Lineages Version'),
        ('status', 'Pangolin QC Status'),
        ('note', 'Pangolin QC Note'),
    ]
    df.rename(columns={x: y for x, y in pangolin_cols}, inplace=True)
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
