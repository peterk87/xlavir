import json
import logging
import re
from pathlib import Path
from typing import Dict

from xlavir.util import find_file_for_each_sample

logger = logging.getLogger(__name__)

GLOB_PATTERNS = ['**/*.fastp.json']

SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.fastp\.json$'),
]


def parse_total_reads(p: Path) -> int:
    """Parse total number of reads from fastp JSON file"""
    total = 0
    try:
        with open(p) as fh:
            j = json.load(fh)
            total = j['summary']['before_filtering']['total_reads']
    except KeyError as ex:
        logger.error(f'')
    return total


def get_info(basedir: Path) -> Dict[str, int]:
    out = {}
    sample_fastp = find_file_for_each_sample(basedir,
                                             glob_patterns=GLOB_PATTERNS,
                                             sample_name_cleanup=SAMPLE_NAME_CLEANUP)
    for sample, fastp in sample_fastp.items():
        n_total_reads = parse_total_reads(fastp)
        out[sample] = n_total_reads
    return out
