import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Union, List, Optional, Mapping, Callable

import numpy as np

logger = logging.getLogger(__name__)


def find_file_for_each_sample(basedir: Path,
                              glob_patterns: List[str],
                              sample_name_cleanup: Optional[List[Union[str, re.Pattern]]] = None,
                              single_entry_selector_func: Optional[Callable] = None) -> Mapping[str, Path]:
    sample_files = defaultdict(list)
    for glob_pattern in glob_patterns:
        for p in basedir.glob(glob_pattern):
            sample = extract_sample_name(p.name,
                                         remove=sample_name_cleanup)
            sample_files[sample].append(p)
        if sample_files:
            break
    sample_file = {}
    for sample, files in sample_files.items():
        if single_entry_selector_func:
            sample_file[sample] = single_entry_selector_func(files)
        else:
            # select first file if no selector func specified
            sample_file[sample] = files[0]
    return sample_file


def extract_sample_name(filename: str,
                        remove: List[Union[str, re.Pattern]] = None) -> str:
    if not remove:
        remove = [
            '.trim',
            '.mkD',
            '.sorted',
            '.bam',
            '.flagstat',
            '.stats',
            '.txt',
            '.idxstats',
            '.depths.tsv',
            '-depths.tsv',
            '.tsv',
            '.mosdepth',
            '.per-base',
            '.bed',
            '.gz'
        ]
    out = filename
    for x in remove:
        if isinstance(x, str):
            out = out.replace(x, '')
        elif isinstance(x, re.Pattern):
            out = x.sub('', out)
        else:
            logger.warning(f'Not sure how to use "{x}" (type={type(x)}) for removing '
                           f'non-sample name text from "{filename}". Skipping "{x}". Output="{out}".')
    return out


def get_col_widths(df, index=False, offset=2, max_width: int = None):
    """Calculate column widths based on column headers and contents"""
    if index:
        idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))]) + offset
        if max_width:
            idx_max = min(idx_max, max_width)
        yield idx_max
    for c in df.columns:
        # get max length of column contents and length of column header
        width = np.max([df[c].astype(str).str.len().max() + 1, len(c) + 1]) + offset
        if max_width:
            width = min(width, max_width)
        yield width


def get_row_heights(df, idx, offset=0, multiplier=15):
    """Calculate row heights"""
    # get max number of newlines in the row
    newline_count = np.max(df.loc[idx, :].astype(str).str.count('\n').max())
    if newline_count < 1:
        newline_count = 1
    height = newline_count * multiplier + offset
    logger.debug(f'idx="{idx}" height={height} newline_count={newline_count}')
    return height


def list_get(xs: Optional[List], idx: int, default=None):
    try:
        return xs[idx]
    except (TypeError, IndexError):
        return default
