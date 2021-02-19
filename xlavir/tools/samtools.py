import re
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from pydantic import BaseModel

from xlavir.util import find_file_for_each_sample

GLOB_PATTERNS = ['**/*.flagstat']


class SamtoolsFlagstat(BaseModel):
    sample: str
    n_total_reads: int
    n_mapped_reads: int


def parse_samtools_flagstat(p: Path) -> Tuple[int, int]:
    """Parse total and mapped number of reads from Samtools flagstat file"""
    total = 0
    mapped = 0
    with open(p) as fh:
        for line in fh:
            m = re.match(r'(\d+)', line)
            if m:
                if 'in total' in line:
                    total = int(m.group(1))
                if ' mapped (' in line:
                    mapped = int(m.group(1))
    return total, mapped


def select_flagstat(paths: List[Path]) -> Optional[Path]:
    xs = [(p, parse_samtools_flagstat(p)) for p in paths]
    xs.sort(key=itemgetter(1), reverse=True)
    try:
        return xs[0][0]
    except KeyError:
        return None


def get_info(basedir: Path) -> Dict[str, SamtoolsFlagstat]:
    out = {}
    flagstats = find_file_for_each_sample(basedir,
                                          glob_patterns=GLOB_PATTERNS,
                                          single_entry_selector_func=select_flagstat)
    # if multiple flagstat files are present, get stats from the one with the largest total number of reads
    for sample, flagstat_path in flagstats.items():
        n_total_reads, n_mapped_reads = parse_samtools_flagstat(flagstat_path)
        samtools_flagstat = SamtoolsFlagstat(sample=sample,
                                             n_mapped_reads=n_mapped_reads,
                                             n_total_reads=n_total_reads)
        out[sample] = samtools_flagstat
    return out
