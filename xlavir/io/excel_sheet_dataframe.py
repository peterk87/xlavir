from typing import Optional, Iterable, Union
import pandas as pd

from enum import Enum


class SheetName(str, Enum):
    workflow_info = 'Workflow Info'
    qc_stats = 'Stats & QC'
    consensus = 'Consensus'
    pangolin = 'Pangolin Lineage'
    variants = 'Variants'
    varmap = 'Variant Map'


class ExcelSheetDataFrame:
    def __init__(self,
                 sheet_name: SheetName,
                 df: pd.DataFrame,
                 pd_to_excel_kwargs: dict = None,
                 autofit: bool = True,
                 column_widths: Optional[Iterable[Union[int, float]]] = None,
                 include_header_width: bool = True):
        self.include_header_width = include_header_width
        self.sheet_name = sheet_name
        self.df = df
        self.pd_to_excel_kwargs = pd_to_excel_kwargs or {}
        self.autofit = autofit
        self.column_widths = column_widths
