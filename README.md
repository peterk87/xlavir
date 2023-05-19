# xlavir - Informative Excel reports from viral sequencing Nextflow analysis

[![PyPI](https://img.shields.io/pypi/v/xlavir.svg)](https://pypi.python.org/pypi/xlavir)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xlavir.svg)](https://pypi.python.org/pypi/xlavir)
[![PyPI - License](https://img.shields.io/pypi/l/xlavir.svg)](https://pypi.python.org/pypi/xlavir)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/xlavir.svg)](https://pypi.python.org/pypi/xlavir)
[![PyPI - Status](https://img.shields.io/pypi/status/xlavir.svg)](https://pypi.python.org/pypi/xlavir)
[![CI](https://github.com/peterk87/xlavir/workflows/CI/badge.svg?branch=master)](https://github.com/peterk87/xlavir/actions)

Excel report from viral sequencing data analysis output from the
[nf-core/viralrecon] or [CFIA-NCFAD/nf-virontus] [Nextflow] pipelines.

## Usage

Create an Excel report from a Nextflow pipeline run:

```bash
# e.g. run nf-core/viralrecon Nextflow pipeline against SARS-CoV-2 samples
# sequenced by Illumina using the ARTIC V4.1 protocol
nextflow run nf-core/viralrecon \
  -profile docker \
  --input samplesheet.csv \
  --platform illumina \
  --protocol amplicon \
  --genome 'MN908947.3' \
  --primer_set artic \
  --primer_set_version '4.1' \
  --skip_assembly \
  --outdir viralrecon-results
# create Excel report from Nextflow pipeline run
xlavir viralrecon-results  xlavir-report-viralrecon-results.xlsx
```

See [example report](xlavir-report.xlsx) from test data in `tests/data/tools`.

## Features

* Collect sample results from a [nf-core/viralrecon] or
  [CFIA-NCFAD/nf-virontus] into an Excel report
  * [Samtools] read mapping stats (`flagstat`)
  * [Mosdepth] read mapping coverage information
  * Variant calling information ([SnpEff] and [SnpSift] results, VCF file
    information) from the following variant callers
    * [Bcftools]
    * [iVar]
    * [Medaka]
    * [Nanopolish]
    * [Clair3]
  * Consensus sequences
* QA/QC of sample analysis results (basic PASS/FAIL based on minimum genome
  coverage and depth)
* [Nextflow] workflow execution information
* Prepend worksheets from other Excel documents into the report (e.g. cover
  page/sheet, sample sheet, lab results)
* Add custom images into worksheets with custom names and descriptions (e.g.
  phylogenetic tree figure PNG)

## License

Distributed under the terms of the [MIT] license, "xlavir" is free and open
source software.

## Credits

This package was created with [Cookiecutter] and the
[audreyr/cookiecutter-pypackage] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[nf-core/viralrecon]: https://github.com/nf-core/viralrecon
[CFIA-NCFAD/nf-virontus]: https://github.com/CFIA-NCFAD/nf-virontus/
[Bcftools]: https://www.htslib.org/doc/bcftools.html
[Samtools]: https://samtools.github.io/
[SnpEff]: https://pcingola.github.io/SnpEff/se_introduction/
[SnpSift]: https://pcingola.github.io/SnpEff/ss_introduction/
[Mosdepth]: https://github.com/brentp/mosdepth
[MIT]: https://opensource.org/licenses/MIT
[Nextflow]: https://www.nextflow.io/
[iVar]: https://andersen-lab.github.io/ivar/html/
[Medaka]: https://github.com/nanoporetech/medaka
[Nanopolish]: https://github.com/jts/nanopolish/
[Clair3]: https://github.com/HKU-BAL/Clair3
