"""Main module."""
import logging
from pathlib import Path
from typing import Optional, List

from xlavir import qc
from xlavir.io.excel_sheet_dataframe import ExcelSheetDataFrame, SheetName
from xlavir.tools import mosdepth, samtools, consensus, pangolin, variants
from xlavir.tools.nextflow import exec_report
from xlavir.tools.nextflow.exec_report import to_dataframe

logger = logging.getLogger(__name__)


def run(input_dir: Path,
        quality_reqs: Optional[qc.QualityRequirements],
        pangolin_lineage_csv: Optional[Path] = None) -> List[ExcelSheetDataFrame]:
    if quality_reqs:
        quality_reqs = qc.QualityRequirements()
    nf_exec_info = exec_report.get_info(input_dir)
    sample_depth_info = mosdepth.get_info(input_dir, low_coverage_threshold=quality_reqs.low_coverage_threshold)
    if logger.level == logging.DEBUG:
        for sample, info in sample_depth_info.items():
            logger.debug(info.dict())
    sample_mapping_info = samtools.get_info(input_dir)
    if logger.level == logging.DEBUG:
        for sample, info in sample_mapping_info.items():
            logger.debug(info.dict())

    sample_variants = variants.get_info(input_dir)

    dfs: List[ExcelSheetDataFrame] = []
    df_stats = qc.create_qc_stats_dataframe(sample_depth_info,
                                            sample_mapping_info,
                                            quality_reqs=quality_reqs)
    dfs.append(ExcelSheetDataFrame(sheet_name=SheetName.qc_stats.value,
                                   df=qc.report_format(df_stats,
                                                       low_coverage_threshold=quality_reqs.low_coverage_threshold),
                                   pd_to_excel_kwargs=dict(freeze_panes=(1, 1), na_rep='NA')))
    df_pangolin = pangolin.get_info(basedir=input_dir,
                                    pangolin_lineage_csv=pangolin_lineage_csv)
    if df_pangolin is not None:
        dfs.append(ExcelSheetDataFrame(sheet_name=SheetName.pangolin.value,
                                       df=df_pangolin,
                                       pd_to_excel_kwargs=dict(freeze_panes=(1, 1))))
    if sample_variants:
        df_variants = variants.to_dataframe(sample_variants.values())
        dfs.append(ExcelSheetDataFrame(sheet_name=SheetName.variants.value,
                                       df=df_variants,
                                       pd_to_excel_kwargs=dict(freeze_panes=(1, 1)),
                                       include_header_width=False))
        df_varmap = variants.to_variant_pivot_table(df_variants)
        max_index_length = df_varmap.index.str.len().max()
        dfs.append(ExcelSheetDataFrame(sheet_name=SheetName.varmap.value,
                                       df=df_varmap,
                                       pd_to_excel_kwargs=dict(freeze_panes=(1, 1), na_rep=0.0),
                                       autofit=False,
                                       column_widths=[max_index_length + 2] + [3 for _ in range(df_varmap.columns.size)]))
    dfs.append(ExcelSheetDataFrame(sheet_name=SheetName.consensus.value,
                                   df=consensus.get_info(basedir=input_dir),
                                   pd_to_excel_kwargs=dict(index=None, header=None)))
    if nf_exec_info:
        df_exec_info = to_dataframe(nf_exec_info)
        dfs.append(ExcelSheetDataFrame(sheet_name=SheetName.workflow_info.value,
                                       df=df_exec_info,
                                       autofit=False,
                                       column_widths=(20, 100)))
        logger.debug(df_exec_info)
    else:
        logger.warning(f'Could not find "execution_report.html" in "{input_dir}"!')

    return dfs
