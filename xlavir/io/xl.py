"""Excel spreadsheet IO functions"""
import logging
from copy import copy
from pathlib import Path
from typing import List, Optional

import openpyxl
import pandas as pd
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from xlavir.images import SheetImage
from xlavir.io.excel_sheet_dataframe import ExcelSheetDataFrame, SheetName
from xlavir.qc import QualityRequirements
from xlavir.util import get_col_widths, get_row_heights

logger = logging.getLogger(__name__)


def copy_spreadsheet(src_path: Path,
                     dest_path: Path,
                     source_sheet_index: int = 0) -> None:
    """Copy a spreadsheet from a source Excel spreadsheet to a destination spreadsheet.

    All cell values and styles are copied over as well as row heights, column widths, merged cells.

    By default the 1st worksheet is copied over.

    Args:
        src_path (Path): Source Excel spreadsheet path
        dest_path (Path): Destination Excel spreadsheet path
        source_sheet_index (int): Source spreadsheet worksheet index to copy to destination spreadsheet
    """
    src_book = openpyxl.load_workbook(src_path)
    dest_book = openpyxl.load_workbook(dest_path)
    sheet = src_book.worksheets[source_sheet_index]
    new_sheet = dest_book.create_sheet(sheet.title)
    dest_book.move_sheet(new_sheet, offset=(len(dest_book.sheetnames) * -2))
    for k, v in sheet.column_dimensions.items():
        new_sheet.column_dimensions[k] = copy(v)
    new_sheet.merged_cells = copy(sheet.merged_cells)
    for k, v in sheet.row_dimensions.items():
        new_sheet.row_dimensions[k] = copy(v)
    for row in sheet.rows:
        for cell in row:
            new_cell = new_sheet[cell.coordinate]
            new_cell.value = cell.value
            if cell.has_style:
                new_cell.font = copy(cell.font)
                new_cell.border = copy(cell.border)
                new_cell.fill = copy(cell.fill)
                new_cell.number_format = copy(cell.number_format)
                new_cell.protection = copy(cell.protection)
                new_cell.alignment = copy(cell.alignment)
    dest_book.save(filename=dest_path)


def write_xlsx_report(dfs: List[ExcelSheetDataFrame],
                      output_xlsx: Path,
                      quality_reqs: QualityRequirements,
                      images_for_sheets: Optional[List[SheetImage]] = None):
    with pd.ExcelWriter(output_xlsx, engine='xlsxwriter') as writer:
        monospace = dict(font_name='Courier New')
        text_wrap = dict(text_wrap=True)
        float_1dec = dict(num_format='0.0')
        perc_1dec = dict(num_format='0.0%')
        perc_2dec = dict(num_format='0.00%')

        book: Workbook = writer.book
        monospace_fmt = book.add_format(monospace)
        monospace_wrap_fmt = book.add_format({**monospace, **text_wrap})
        monospace_wrap_fmt.set_align('left')
        monospace_wrap_fmt.set_align('top')
        monospace_float_fmt = book.add_format({**monospace, **float_1dec})
        monospace_perc_fmt = book.add_format({**monospace, **perc_1dec})
        monospace_perc_2dec_fmt = book.add_format({**monospace, **perc_2dec})
        header_with_wrap_fmt = book.add_format({**text_wrap,
                                                'bold': True,
                                                'border': 1,
                                                'align': 'center',
                                                'valign': 'top'})
        varmap_header_fmt = book.add_format(dict(border=1,
                                                 align='left',
                                                 valign='bottom',
                                                 rotation=45,
                                                 font_name='Courier New'))
        red_bg_fmt = book.add_format(dict(bg_color='red'))
        float_cols = {'Mean Coverage Depth'}
        perc_cols = {'% Genome Coverage'}
        perc_2dec_cols = {'Alternate Allele Frequency'}

        for esdf in dfs:
            esdf.df.to_excel(writer, sheet_name=esdf.sheet_name, **esdf.pd_to_excel_kwargs)

            sheet: Worksheet = book.get_worksheet_by_name(esdf.sheet_name)

            idx_and_cols = [esdf.df.index.name] + list(esdf.df.columns)
            if esdf.autofit:
                for i, (width, col_name) in enumerate(zip(get_col_widths(esdf.df,
                                                                         index=True,
                                                                         max_width=80,
                                                                         include_header=esdf.include_header_width),
                                                          idx_and_cols)):
                    if col_name in float_cols:
                        sheet.set_column(i, i, width, monospace_float_fmt)
                    elif col_name in perc_cols:
                        sheet.set_column(i, i, width, monospace_perc_fmt)
                    elif col_name in perc_2dec_cols:
                        sheet.set_column(i, i, width, monospace_perc_2dec_fmt)
                    else:
                        sheet.set_column(i, i, width, monospace_fmt)
                if not esdf.include_header_width:
                    for i, col_name in enumerate(idx_and_cols):
                        sheet.write_string(0, i, string=col_name, cell_format=header_with_wrap_fmt)

            elif esdf.column_widths:
                for i, (width, col_name) in enumerate(zip(esdf.column_widths, idx_and_cols)):
                    sheet.set_column(i, i, width, monospace_wrap_fmt)

                for i, idx in enumerate(esdf.df.index, 1):
                    sheet.set_row(i, get_row_heights(esdf.df, idx), monospace_wrap_fmt)

            if esdf.sheet_name == SheetName.varmap.value:
                sheet.set_row(0, max(len(x) for x in idx_and_cols)*5)
                for i, col_name in enumerate(idx_and_cols):
                    if i == 0:
                        continue
                    sheet.write_string(0, i, string=col_name, cell_format=varmap_header_fmt)
                sheet.conditional_format(first_row=1,
                                         first_col=1,
                                         last_row=esdf.df.shape[0],
                                         last_col=esdf.df.shape[1],
                                         options=dict(type='3_color_scale',
                                                      min_type='num',
                                                      mid_type='num',
                                                      max_type='num',
                                                      min_value=0.0,
                                                      mid_value=quality_reqs.major_allele_freq,
                                                      max_value=1.0))

            if esdf.sheet_name == SheetName.consensus.value:
                sheet.hide_gridlines(2)
                sheet.hide_row_col_headers()

            if esdf.sheet_name == SheetName.qc_stats.value:
                logger.info(f'Setting red background color for QC Status column of sheet "{esdf.sheet_name}"')
                sheet.conditional_format(1, 1, esdf.df.shape[0], 1, options=dict(type='cell',
                                                                                 value='"FAIL"',
                                                                                 criteria='equal to',
                                                                                 format=red_bg_fmt))
        if images_for_sheets:
            add_images(images_for_sheets, book)


def add_images(images_for_sheets: List[SheetImage],
               book: Workbook):
    text_wrap_fmt = book.add_format(dict(text_wrap=True))
    text_wrap_fmt.set_align('vjustify')
    for sheet_image in images_for_sheets:
        sheet = book.add_worksheet(sheet_image.sheet_name)
        sheet.set_column(0, 0, 100, text_wrap_fmt)
        sheet.write(0, 0, sheet_image.image_description, text_wrap_fmt)
        sheet.insert_image(1, 0, sheet_image.image_path)
        sheet.hide_gridlines(2)
        sheet.hide_row_col_headers()
