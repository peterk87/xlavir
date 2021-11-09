import logging
import re
from pathlib import Path
from typing import List, Mapping

import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from xlavir.util import find_file_for_each_sample

SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.AF0\.\d+'),
    '.consensus',
    '.fasta',
    '.fa',
]

GLOB_PATTERNS = [
    '**/ivar/**/*.consensus.fa*',
    '**/*.consensus.fa*'
]

logger = logging.getLogger(__name__)


def chunk(s: str, n: int = 80) -> List[str]:
    """Chunk string into segments of specified length.

    >>> chunk(('wordsX' * 5), 11)
    ['wordsXwords', 'XwordsXword', 'sXwordsX']
    >>> chunk('x', 80)
    ['x']
    """
    return [s[i:i + n] for i in range(0, len(s), n)]


def read_fasta(sample: str, path: Path) -> List[str]:
    out = []
    rec: SeqRecord
    for idx, rec in enumerate(SeqIO.parse(path, format='fasta')):
        out.append(f'>{sample}' if idx == 0 else f'>{sample}-{idx}')
        seq = str(rec.seq)
        # if length of seq is over Excel cell character limit (32,767)
        # then chunk seq up into 80 character chunks
        out += chunk(seq, 80) if len(seq) > 32000 else [seq]
    return out


def fasta_dataframe(sample_fasta: Mapping[str, Path]) -> pd.DataFrame:
    df = pd.DataFrame()
    fasta_list = []
    for sample in sorted(sample_fasta.keys()):
        fasta_path = sample_fasta[sample]
        fasta_list += read_fasta(sample, fasta_path)
    df['fasta'] = fasta_list
    return df


def get_info(basedir: Path) -> pd.DataFrame:
    sample_fasta = find_file_for_each_sample(basedir,
                                             glob_patterns=GLOB_PATTERNS,
                                             sample_name_cleanup=SAMPLE_NAME_CLEANUP)
    return fasta_dataframe(sample_fasta)
