from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from pydantic import BaseModel

from xlavir.util import find_file_for_each_sample

SAMPLE_NAME_CLEANUP = [
    '.genome.per-base.bed.gz',
    '.per-base.bed.gz',
    '.bam',
    '.trim',
    '.mkD',
    '.fgbio',
    '.clipbam',
    '.ivar_trim',
    '.sorted',
    '.sort',
    '.bam',
]

GLOB_PATTERNS = [
    '**/mosdepth/**/*.genome.per-base.bed.gz',
    '**/mosdepth/**/*.per-base.bed.gz',
    # fallback to parsing BAM files
    '**/*.trim*.bam',
    '**/*.bam',
]


class MosdepthDepthInfo(BaseModel):
    """Depth information for a sample."""
    sample: str
    n_zero_coverage: int
    zero_coverage_coords: str
    low_coverage_threshold: int = 5
    n_low_coverage: int
    low_coverage_coords: str
    genome_coverage: float
    mean_coverage: float
    median_coverage: int
    ref_seq_length: int


def read_mosdepth_bed(p: Path) -> pd.DataFrame:
    """Read Mosdepth per-base bed file."""
    return pd.read_table(p, header=None, names=['genome', 'start_idx', 'end_idx', 'depth'])


def get_interval_coords(depths: np.ndarray, threshold: int = 0) -> str:
    """Get coordinates of intervals where depth is zero or below threshold if specified.

    >>> get_interval_coords(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    '1-10'
    >>> get_interval_coords(np.array([0,1,2,3,4,0,0,0,1,2,3,4,5,6,0,0]))
    '1; 6-8; 15-16'
    >>> get_interval_coords(np.array([0,1,2,3,4,0,0,0,1,2,3,4,5,6,0,0]), threshold=2)
    '1-2; 6-9; 15-16'

    Args:
        depths: Coverage depths array
        threshold: Minimum depth threshold

    Returns:
        Coordinates of intervals where depth is zero or below threshold
    """
    mask = depths == 0 if threshold == 0 else depths < threshold
    below = np.where(mask)[0]
    coords: list[list[int]] = []
    for x in below:
        if coords:
            last = coords[-1][-1]
            if x == last + 1:
                coords[-1].append(x)
            else:
                coords.append([x])
        else:
            coords.append([x])
    return '; '.join([f'{xs[0] + 1}-{xs[-1] + 1}' if xs[0] != xs[-1] else f'{xs[0] + 1}' for xs in coords])


def get_genome_coverage(depths: np.ndarray, low_coverage_threshold: int = 5) -> float:
    """Calculate genome coverage as a fraction of positions with depth >= low_coverage_threshold

    >>> get_genome_coverage(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    0.0
    >>> get_genome_coverage(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 5]))
    0.1
    >>> get_genome_coverage(np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]))
    0.6

    Args:
        depths: Coverage depths array
        low_coverage_threshold: Minimum depth threshold

    Returns:
        Genome coverage as a fraction of positions with depth >= low_coverage_threshold
    """
    return 1.0 - (np.count_nonzero(depths < low_coverage_threshold) / len(depths))


def depth_array(df: pd.DataFrame) -> np.ndarray:
    """Convert Mosdepth per-base bed file to depth array.

    >>> depth_array(pd.DataFrame({'start_idx': [0, 3, 6], 'end_idx': [3, 6, 10], 'depth': [1, 2, 3]}))
    array([1, 1, 1, 2, 2, 2, 3, 3, 3, 3])
    """
    arr = np.zeros(df.end_idx.max())
    for row in df.itertuples():
        arr[row.start_idx:row.end_idx] = row.depth
    return arr


def parse_bam_depths(bam_path: Path) -> np.ndarray:
    """Parse BAM file for depths of coverage across first reference genome using pysam

    Args:
        bam_path: Path to BAM file

    Returns:
        Coverage depths
    """
    import pysam
    bam = pysam.AlignmentFile(bam_path)
    reference_name = bam.references[0]
    reference_length = bam.get_reference_length(reference_name)
    depths = np.zeros(reference_length, dtype=np.int32)
    for pileupcolumn in bam.pileup():
        depth = sum(
            1
            for pileupread in pileupcolumn.pileups
            if not (pileupread.is_del or pileupread.is_refskip)
        )
        depths[pileupcolumn.reference_pos] = depth
    return depths


def get_info(basedir: Path, low_coverage_threshold: int = 5) -> Dict[str, MosdepthDepthInfo]:
    """Get depth information for each sample in a Nextflow output directory."""
    sample_paths = find_file_for_each_sample(basedir,
                                             glob_patterns=GLOB_PATTERNS,
                                             sample_name_cleanup=SAMPLE_NAME_CLEANUP)
    out = {}
    for sample, path in sample_paths.items():
        # fallback to parsing BAM files if Mosdepth BED files are not found
        if path.suffix == '.bam':
            arr = parse_bam_depths(path)
        else:  # Mosdepth BED file
            df = read_mosdepth_bed(path)
            arr = depth_array(df)
        mean_cov = arr.mean()
        median_cov = pd.Series(arr).median()
        depth_info = MosdepthDepthInfo(sample=sample,
                                       low_coverage_threshold=low_coverage_threshold,
                                       n_low_coverage=np.sum(arr < low_coverage_threshold),
                                       n_zero_coverage=np.sum(arr == 0),
                                       zero_coverage_coords=get_interval_coords(arr),
                                       low_coverage_coords=get_interval_coords(arr, low_coverage_threshold),
                                       genome_coverage=get_genome_coverage(arr, low_coverage_threshold),
                                       mean_coverage=mean_cov,
                                       median_coverage=median_cov,
                                       ref_seq_length=len(arr))
        out[sample] = depth_info
    return out
