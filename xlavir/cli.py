"""Console script for xlavir."""
import logging
from enum import Enum
from pathlib import Path
from typing import Optional, List
from sys import version_info

import typer
from rich.logging import RichHandler
import pandas as pd

from xlavir import __version__
from xlavir.images import get_images_for_sheets
from xlavir.io.excel_sheet_dataframe import ExcelSheetDataFrame, SheetName
from xlavir.qc import QualityRequirements
from xlavir.xlavir import run
from xlavir.io.xl import write_xlsx_report

app = typer.Typer()


class QCPresets(str, Enum):
    default = 'default'
    scov2_illumina = 'scov2_illumina'
    scov2_nanopore = 'scov2_nanopore'


qc_presets = dict(
    default=QualityRequirements(),
    scov2_illumina=QualityRequirements(
        min_genome_coverage=0.95,
        min_median_depth=30,
        low_coverage_threshold=5,
    ),
    scov2_nanopore=QualityRequirements(
        min_genome_coverage=0.95,
        min_median_depth=50,
        low_coverage_threshold=10,
    )
)


def version_callback(value: bool):
    if value:
        typer.echo(f"xlavir version {__version__}")
        raise typer.Exit()


def check_dir_exists_callback(path: Path) -> Path:
    if not (path.exists() or path.is_dir()):
        raise typer.BadParameter(f'An existing Nextflow workflow results directory must be specified! '
                                 f'"{path}" does not exist or is not a directory!')
    return path


@app.command(
    epilog=f'xlavir version {__version__}; Python {version_info.major}.{version_info.minor}.{version_info.micro}')
def main(
        input_dir: Path = typer.Argument(..., callback=check_dir_exists_callback),
        output: Path = typer.Argument('xlavir-report.xlsx'),
        ct_table: Path = typer.Option(None, help='Table of sample IDs and rtPCR Ct values'),
        pangolin_lineage_csv: Path = typer.Option(None, help='Pangolin lineage report CSV'),
        qc_preset: Optional[QCPresets] = typer.Option(None, help='Quality check preset'),
        low_coverage_threshold: Optional[int] = typer.Option(None, help='Low coverage threshold. '
                                                                        'Used for calculation of % genome coverage.'),
        min_genome_coverage: Optional[float] = typer.Option(None, help='Min genome coverage. e.g. 0.95 == 95%'),
        min_median_depth: Optional[int] = typer.Option(None, help='Min median coverage depth'),
        major_allele_freq: float = typer.Option(0.75, help='Major alternate allele fraction'),
        spreadsheet: Optional[List[Path]] = typer.Option(None, help='Copy Excel worksheet from workbook. '
                                                                    'Can specify multiple.'),
        image: Optional[List[Path]] = typer.Option(None, help="Image path for image to add to sheet. "
                                                              "Can specify multiple."),
        image_title: Optional[List[str]] = typer.Option(None, help="Image sheet title"),
        image_description: Optional[List[str]] = typer.Option(None, help="Image description."),
        verbose: bool = typer.Option(default=False, help='Verbose logging'),
        version: Optional[bool] = typer.Option(None, callback=version_callback,
                                               help=f'Print "xlavir version {__version__}" and exit'),
):
    """xlavir - create an Excel report from a bioinformatics analysis output directory

    Typical usage:

    $ xlavir /path/to/viralrecon-or-virontus-results

    Will output "report.xlsx" in current directory.

    Specify report output filename:

    $ xlavir /path/to/viralrecon-or-virontus-results xlavir-run-XXXX.xlsx

    """
    from rich.traceback import install
    install(show_locals=True, width=120, word_wrap=True)

    logging.basicConfig(format='%(message)s',
                        datefmt='[%Y-%m-%d %X]',
                        level=logging.INFO if not verbose else logging.DEBUG,
                        handlers=[RichHandler(rich_tracebacks=True,
                                              tracebacks_show_locals=True)])

    images_for_sheets = None
    if image:
        images_for_sheets = get_images_for_sheets(image, image_title, image_description)

    quality_reqs = qc_presets[QCPresets.default.value]
    if qc_preset:
        quality_reqs = qc_presets[qc_preset.value]
    if min_genome_coverage:
        quality_reqs.min_genome_coverage = min_genome_coverage
    if low_coverage_threshold:
        quality_reqs.low_coverage_threshold = low_coverage_threshold
    if min_median_depth:
        quality_reqs.min_median_depth = min_median_depth
    if major_allele_freq:
        quality_reqs.major_allele_freq = major_allele_freq

    dfs = run(input_dir=input_dir,
              pangolin_lineage_csv=pangolin_lineage_csv,
              ct_values_table=ct_table,
              quality_reqs=quality_reqs)
    dfs.append(ExcelSheetDataFrame(
        sheet_name=SheetName.xlavir_info.value,
        df=pd.DataFrame([
            ('xlavir version', __version__),
            ('Python version', f'{version_info.major}.{version_info.minor}.{version_info.micro}'),
            ('Input directory', input_dir.absolute()),
            ('QC Requirements', quality_reqs),
        ], columns=['Attribute', 'Value']).set_index('Attribute')
    ))
    write_xlsx_report(dfs=dfs,
                      output_xlsx=output,
                      quality_reqs=quality_reqs,
                      images_for_sheets=images_for_sheets)
    if spreadsheet:
        from xlavir.io.xl import copy_spreadsheet
        for excel in spreadsheet:
            copy_spreadsheet(excel, output)

    return 0


if __name__ == "__main__":
    app()  # pragma: no cover
