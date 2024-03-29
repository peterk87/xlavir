import contextlib
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Union, List, Optional, Mapping, Callable, Iterator

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def find_file_for_each_sample(
        basedir: Path,
        glob_patterns: List[str],
        sample_name_cleanup: Optional[List[Union[str, re.Pattern]]] = None,
        single_entry_selector_func: Optional[Callable] = None
) -> Mapping[str, Path]:
    sample_files = defaultdict(list)
    for glob_pattern in glob_patterns:
        for p in basedir.glob(glob_pattern):
            sample = extract_sample_name(p.name,
                                         remove=sample_name_cleanup)
            sample_files[sample].append(p)
    return {
        sample: single_entry_selector_func(files)
        if single_entry_selector_func
        else files[0]
        for sample, files in sample_files.items()
    }


def extract_sample_name(
        filename: str,
        remove: Optional[List[Union[str, re.Pattern]]] = None
) -> str:
    if not remove:
        remove = [
            '.pass',
            '.mapped',
            '.trim',
            '.ivar_trim',
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


def get_col_widths(
        df: pd.DataFrame,
        index=False,
        offset=2,
        max_width: Optional[int] = None,
        include_header=True
) -> Iterator[int]:
    """Calculate column widths based on column headers and contents"""
    if index:
        idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))]) + offset
        if max_width:
            idx_max = min(idx_max, max_width)
        yield idx_max
    for c in df.columns:
        # get max length of column contents and length of column header
        max_width_cells = df[c].astype(str).str.len().max() + 1
        if include_header:
            width = np.max([max_width_cells, len(c) + 1]) + offset
        elif isinstance(c, str):
            col_words = c.split()
            col_words.sort(key=len, reverse=True)
            max_word_size = int(len(col_words[-1]) * 1.25 + 1)
            width = np.max([max_width_cells, max_word_size]) + offset
        else:
            width = max_width_cells + offset
        if max_width:
            width = min(width, max_width)
        yield width


def get_row_heights(
        df: pd.DataFrame,
        idx: Union[str, int],
        offset=0,
        multiplier=15
) -> int:
    """Calculate row heights"""
    # get max number of newlines in the row
    newline_count = np.max(df.loc[idx, :].astype(str).str.count('\n').max())
    newline_count = max(newline_count, 1)
    height = newline_count * multiplier + offset
    logger.debug(f'idx="{idx}" height={height} newline_count={newline_count}')
    return height


def list_get(
        xs: Optional[List],
        idx: int,
        default=None
) -> Optional[Union[str, int, float, List[Union[str, int, float]]]]:
    if xs is None:
        return default
    try:
        return xs[idx]
    except (TypeError, IndexError):
        return default


def try_parse_number(s: str) -> Union[int, float, str, List[Union[float, int, str]]]:
    if ',' in s:
        xs = s.split(',')
        return [try_parse_number(x) for x in xs] # type: ignore[misc]
    with contextlib.suppress(ValueError):
        return int(s)
    with contextlib.suppress(ValueError):
        return float(s)
    return s
