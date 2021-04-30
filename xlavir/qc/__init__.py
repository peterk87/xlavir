import logging
from typing import Dict, List, Tuple

import pandas as pd

from xlavir.qc.quality_requirements import QualityRequirements
from xlavir.tools import mosdepth, samtools

logger = logging.getLogger(__name__)


def columns(low_coverage_threshold: int = 5) -> List[Tuple[str, str]]:
    return [
        ('sample', 'Sample', 'Sample name'),
        ('ct_value', 'Ct Value', 'Real-time PCR Ct value'),
        (
            'qc_status',
            'QC Status',
            'Quality control status, i.e. PASS or FAIL based on QC criteria '
            'such as minimum mean read depth '
            'or percent of reference genome covered by sequencing'
        ),
        (
            'qc_comment',
            'QC Comment',
            'Comments on any potential quality issues, i.e. why a sample did not pass QC.'
        ),
        (
            'genome_coverage',
            '% Genome Coverage',
            'Percent of reference genome sequence covered by sequencing'
        ),
        (
            'mean_coverage',
            'Mean Coverage Depth',
            'Mean sequencing coverage depth across entire reference genome sequence.'
        ),
        (
            'median_coverage',
            'Median Coverage Depth',
            'Median sequencing coverage depth across entire reference genome sequence.',
        ),
        (
            'n_total_reads',
            '# Total Reads',
            'Total number of raw reads obtained from sequencing for this sample.'
        ),
        (
            'n_mapped_reads',
            '# Mapped Reads',
            'Number of sequencing reads that mapped to the reference genome sequence.'
        ),
        (
            'n_zero_coverage',
            '# 0X positions',
            'Number of reference sequence positions with no coverage depth (0X), i.e. '
            'reference positions that did not have any reads spanning those positions.'
        ),
        (
            'n_low_coverage',
            f'# <{low_coverage_threshold}X positions',
            f'Number of reference sequence positions with fewer than {low_coverage_threshold} reads'
            f' spanning those positions.'
        ),
        (
            'ref_seq_length',
            'Reference Sequence Length',
            'Reference sequence length'
        ),
        (
            'zero_coverage_coords',
            '0X Coverage Regions',
            'A list of reference sequence 1-based regions with no coverage (0X).'
        ),
        (
            'low_coverage_coords',
            f'<{low_coverage_threshold}X Coverage Regions',
            f'A list of reference sequence 1-based regions with less than {low_coverage_threshold}'
            f' coverage depth.'
        ),
    ]


def report_format(df: pd.DataFrame, low_coverage_threshold: int = 5) -> pd.DataFrame:
    output_cols = columns(low_coverage_threshold)
    df.rename(columns={x: y for x, y, _ in output_cols}, inplace=True)
    df.set_index('Sample', inplace=True)
    return df


def create_qc_stats_dataframe(sample_depth_info: Dict[str, mosdepth.MosdepthDepthInfo],
                              sample_mapping_info: Dict[str, samtools.SamtoolsFlagstat],
                              sample_cts: Dict[str, float],
                              quality_reqs: QualityRequirements):
    sample_names = set(sample_depth_info.keys()) | set(sample_mapping_info.keys())
    logger.info(f'N samples: {len(sample_names)}')
    merged_stats_info = {}
    for sample in sample_names:
        depth_info = sample_depth_info[sample].dict() if sample in sample_depth_info else {}
        mapping_info = sample_mapping_info[sample].dict() if sample in sample_mapping_info else {}
        merged_stats_info[sample] = {**depth_info, **mapping_info}
        merged_stats_info[sample]['ct_value'] = sample_cts.get(sample, None)
    df_stats = pd.DataFrame(merged_stats_info.values())
    mask_pass_depth = (df_stats.median_coverage >= quality_reqs.min_median_depth)
    mask_pass_breadth = (df_stats.genome_coverage >= quality_reqs.min_genome_coverage)
    qc_pass_mask = mask_pass_depth & mask_pass_breadth
    df_stats['qc_status'] = 'FAIL'
    df_stats.loc[qc_pass_mask, 'qc_status'] = 'PASS'
    qc_comments = []
    for i, (pass_depth, pass_breadth) in enumerate(zip(mask_pass_depth, mask_pass_breadth)):
        comments = []
        if not pass_depth:
            comments += [f'Median depth below {quality_reqs.min_median_depth}']
        if not pass_breadth:
            comments += [f'Genome coverage below {quality_reqs.min_genome_coverage:.0%}']
        qc_comments.append('; '.join(comments))
    df_stats['qc_comment'] = qc_comments
    df_stats.loc[mask_pass_breadth, 'qc_comment'] = ''
    df_stats.sort_values('sample', inplace=True)

    present_cols = set(df_stats.columns)
    output_cols = columns(quality_reqs.low_coverage_threshold)
    df_stats = df_stats.loc[:, [x for x, y, _ in output_cols if x in present_cols]]

    logger.debug(df_stats)
    return df_stats
