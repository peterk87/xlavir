import logging
import re
from pathlib import Path
from typing import List, Mapping

import pandas as pd
from Bio import SeqIO

from ..util import find_file_for_each_sample

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


def read_fasta(sample: str, path: Path) -> List[str]:
    out = []
    for rec in SeqIO.parse(path, format='fasta'):
        out += [f'>{sample}', str(rec.seq)]
    if len(out) > 2:
        logger.info(f'More than 1 sequence in consensus sequence for sample "{sample}". '
                    f'Appending sequence index starting at 1.')
        for idx, i in enumerate(range(0, len(out), 2)):
            out[i] = f'>{sample}-{idx + 1}'
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
