from typing import Dict

import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def validate_ct_table(df: pd.DataFrame) -> bool:
    if df.empty:
        logger.error(f'Ct values table is empty! No Ct values present!')
        return False
    n_rows, n_cols = df.shape
    if n_cols != 2:
        logger.error(
            f'Ct values table expected to only have 2 columns, but {n_cols} were found with names: {", ".join(df.columns)}')
        return False
    return True


def read_ct_table(ct_path: Path) -> Dict[str, float]:
    suffix = ct_path.suffix.lower()
    if suffix == '.txt':
        logger.warning(f'Trying to read "{ct_path.name}" as tab-delimited file with header.')
        df = pd.read_table(ct_path)
    elif suffix == '.tsv':
        df = pd.read_table(ct_path)
    elif suffix == '.ods':
        df = pd.read_excel(ct_path, engine='odf')
    elif suffix == '.csv':
        df = pd.read_csv(ct_path)
    elif suffix == '.xlsx':
        df = pd.read_excel(ct_path)
    else:
        logger.error(f'Not sure how to parse Ct values table with extension "{suffix}". '
                     f'Please provide a tab-delimited file (".tsv"), CSV (".csv"), '
                     f'Excel file (".xlsx") or OpenDocument Spreadsheet (".ods").')
        return {}
    if validate_ct_table(df):
        df.columns = ['sample', 'ct']
        logger.info(f'Read table with shape {df.shape} from "{ct_path}"')
        return {row.sample: row.ct for row in df.itertuples()}
    else:
        return {}
