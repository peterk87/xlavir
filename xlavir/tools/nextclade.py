import logging
import re
from pathlib import Path
from typing import Dict

import pandas as pd

from xlavir.util import find_file_for_each_sample

logger = logging.getLogger(__name__)

nextclade_cols = [
    (
        'seqName',
        'Sample',
        'Sample name.',
    ),
    (
        'clade',
        'Clade',
        'The result of the clade assignment of a sequence, as defined by Nextstrain. ',
    ),
    # STATUS
    (
        'qc.overallStatus',
        'QC: Overall Status',
        'Overall quality control assessment status by Nextclade',
    ),
    (
        'qc.missingData.status',
        'QC: Missing Data Status',
        'Missing data status according to Nextclade quality control assessment.',
    ),
    (
        'qc.mixedSites.status',
        'QC: Mixed Sites Status',
        'Mixed sites status according to Nextclade quality control assessment.',
    ),
    (
        'qc.privateMutations.status',
        'QC: Private Mutations Status',
        'Private mutations status according to Nextclade quality control assessment.',
    ),
    (
        'qc.snpClusters.status',
        'QC: Mutation Clusters Status',
        'Mutation clusters status according to Nextclade quality control assessment.',
    ),
    # TOTALS
    (
        'totalGaps',
        '# Gaps',
        'Number of `-` characters (gaps) in the sequence.',
    ),
    (
        'totalInsertions',
        '# Insertions',
        'Number of insertions in the sequence.',
    ),
    (
        'totalMissing',
        '# Missing',
        'Number of missing sites in the sequence.',
    ),
    (
        'totalMutations',
        '# Mutations',
        'Number of mutations in the sequence relative to Wuhan-Hu-1 (MN908947.3) SARS-CoV-2 sequence.',
    ),
    (
        'totalNonACGTNs',
        '# non-ACGTN',
        'Number of non-nucleotide (A, C, G, or T) or N characters in the sequence.',
    ),
    (
        'totalPcrPrimerChanges',
        '# PCR primer changes',
        'Total number of changes to known PCR primers as a result of mutations.',
    ),
    (
        'totalAminoacidSubstitutions',
        '# Amino Acid Substitutions',
        'Number of amino acid substitution mutations in the sequence.',
    ),
    (
        'totalAminoacidDeletions',
        '# Amino Acid Deletions',
        'Number of amino acid deletion mutations in the sequence.',
    ),
    (
        'qc.missingData.totalMissing',
        'QC: # Missing Data',
        'Number of missing data sites according to Nextclade quality control assessment.',
    ),
    (
        'qc.mixedSites.totalMixedSites',
        'QC: # Mixed Sites',
        'Number of mixed sites according to Nextclade quality control assessment.',
    ),
    (
        'qc.privateMutations.total',
        'QC: # Private Mutations',
        'Number of private mutations according to Nextclade quality control assessment.',
    ),
    (
        'qc.snpClusters.totalSNPs',
        'QC: # Mutation Clusters',
        'Number of mutation clusters according to Nextclade quality control assessment.',
    ),
    (
        'qc.privateMutations.excess',
        'QC: Private Mutations Excess',
        'Number of excess private mutations according to Nextclade quality control assessment.',
    ),
    # LISTS
    (
        'substitutions',
        'Substitutions',
        'List of substitution mutations in the sequence.',
    ),
    (
        'deletions',
        'Deletions',
        'List of deletion mutations in the sequence.',
    ),
    (
        'insertions',
        'Insertions',
        'List of insertion mutations in the sequence.',
    ),
    (
        'missing',
        'Missing',
        'List of missing sites in the sequence.',
    ),
    (
        'nonACGTNs',
        'nonACGTNs',
        'List of non-ACGTN sites in the sequence.',
    ),
    (
        'pcrPrimerChanges',
        'PCR primer changes',
        'List of PCR primer changes in the sequence.',
    ),
    (
        'aaSubstitutions',
        'Amino Acid Substitutions',
        'List of amino acid substitution mutations in the sequence.',
    ),
    (
        'aaDeletions',
        'Amino Acid Deletions',
        'List of amino acid deletion mutations in the sequence.',
    ),
    (
        'qc.snpClusters.clusteredSNPs',
        'QC: Mutation Clusters',
        'Clustered mutations according to Nextclade quality control assessment.',
    ),
    # THRESHOLDS
    (
        'qc.missingData.missingDataThreshold',
        'QC: Missing Data Threshold',
        'Missing data threshold according to Nextclade quality control assessment.',
    ),
    (
        'qc.mixedSites.mixedSitesThreshold',
        'QC: Mixed Sites Threshold',
        'Threshold for number of mixed sites for Nextclade quality control assessment.',
    ),
    (
        'qc.privateMutations.cutoff',
        'QC: Private Mutations Cutoff',
        'Cutoff for number of private mutations for Nextclade quality control assessment.',
    ),
    # SCORE
    (
        'qc.overallScore',
        'QC: Overall Score',
        'Overall quality control assessment score by Nextclade',
    ),
    (
        'qc.missingData.score',
        'QC: Missing Data Score',
        'Missing data score according to Nextclade quality control assessment.',
    ),
    (
        'qc.mixedSites.score',
        'QC: Mixed Sites Score',
        'Mixed sites score according to Nextclade quality control assessment.',
    ),
    (
        'qc.privateMutations.score',
        'QC: Private Mutations Score',
        'Private mutations score according to Nextclade quality control assessment.',
    ),
    (
        'qc.snpClusters.score',
        'QC: Mutation Clusters Score',
        'Mutation clusters score according to Nextclade quality control assessment.',
    ),
    # ALIGNMENT
    (
        'alignmentEnd',
        'Alignment End',
        'Nextalign alignment end index.',
    ),
    (
        'alignmentScore',
        'Alignment Score',
        'Nextalign alignment score.',
    ),
    (
        'alignmentStart',
        'Alignment Start',
        'Nextalign alignment start.',
    ),
    (
        'errors',
        'Nextclade errors',
        'Nextclade errors',
    ),
]

NEXTCLADE_GLOB_PATTERNS = [
    '**/nextclade/*.csv'
]

NEXTCLADE_SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.csv$')
]


def read_nextclade_csv(path: Path, sample_name: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=';')
    df.rename(columns={x: y for x, y, _ in nextclade_cols}, inplace=True)
    df['Sample'] = sample_name
    return df


def get_info(basedir: Path) -> Dict[str, pd.DataFrame]:
    sample_nextclade = find_file_for_each_sample(basedir=basedir,
                                                 glob_patterns=NEXTCLADE_GLOB_PATTERNS,
                                                 sample_name_cleanup=NEXTCLADE_SAMPLE_NAME_CLEANUP)
    logger.info(f'Found {len(sample_nextclade)} Nextclade CSV files. Parsing...')
    out = {}
    for sample, nextclade_path in sample_nextclade.items():
        out[sample] = read_nextclade_csv(nextclade_path, sample)
    return out


def to_dataframe(sample_nextclade: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = pd.concat(list(sample_nextclade.values()))
    df.sort_values('Sample', inplace=True)
    df.set_index('Sample', inplace=True)
    return df[[x for _,x,_ in nextclade_cols if x in df.columns]]
