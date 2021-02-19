import logging
from typing import Dict, List, Tuple

import pandas as pd

from xlavir.qc.quality_requirements import QualityRequirements
from xlavir.tools import mosdepth, samtools

logger = logging.getLogger(__name__)


def column_rename_tuple(low_coverage_threshold: int = 5) -> List[Tuple[str, str]]:
    return [
        ('sample', 'Sample'),
        ('qc_status', 'QC Status'),
        ('qc_comment', 'QC Comment'),
        ('genome_coverage', '% Genome Coverage'),
        ('mean_coverage', 'Mean Coverage Depth'),
        ('median_coverage', 'Median Coverage Depth'),
        ('n_total_reads', '# Total Reads'),
        ('n_mapped_reads', '# Mapped Reads'),
        ('n_zero_coverage', '# 0X positions'),
        ('n_low_coverage', f'# <{low_coverage_threshold}X positions'),
        ('zero_coverage_coords', '0X Coverage Regions'),
        ('low_coverage_coords', f'<{low_coverage_threshold}X Coverage Regions'),
    ]


def report_format(df: pd.DataFrame, low_coverage_threshold: int = 5) -> pd.DataFrame:
    output_cols = column_rename_tuple(low_coverage_threshold)
    df.rename(columns={x: y for x, y in output_cols}, inplace=True)
    df.set_index('Sample', inplace=True)
    return df


def create_qc_stats_dataframe(sample_depth_info: Dict[str, mosdepth.MosdepthDepthInfo],
                              sample_mapping_info: Dict[str, samtools.SamtoolsFlagstat],
                              quality_reqs: QualityRequirements):
    sample_names = set(sample_depth_info.keys()) | set(sample_mapping_info.keys())
    logger.info(f'N samples: {len(sample_names)}')
    merged_stats_info = {}
    for sample in sample_names:
        depth_info = sample_depth_info[sample].dict() if sample in sample_depth_info else {}
        mapping_info = sample_mapping_info[sample].dict() if sample in sample_mapping_info else {}
        merged_stats_info[sample] = {**depth_info, **mapping_info}
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
    output_cols = column_rename_tuple(quality_reqs.low_coverage_threshold)
    df_stats = df_stats.loc[:, [x for x, y in output_cols if x in present_cols]]

    logger.debug(df_stats)
    return df_stats
