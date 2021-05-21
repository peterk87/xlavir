=======
History
=======

0.4.2 (2021-05-21)
------------------

* Add support for nf-core/viralrecon version 2.0 (requires Mosdepth ``bed.gz`` files be output; needs custom ``modules.config`` like `this one <https://gist.github.com/peterk87/495621349c1161d12047c1c8f97935af>`_)
* `Nextclade CLI <https://github.com/nextstrain/nextclade/blob/master/packages/cli/README.md>`_ per sample results parsed into sheet showing useful info like Nextstrain clade, # of mutations, # of PCR primer changes
* Added check that input directory exists and is a directory
* Added sheet with xlavir info
* Added Gene, Variant Effect, Variant Impact, Amino Acid Change to Variant Summary table


0.4.1 (2021-05-14)
------------------

* Add reference sequence length to QC stats table. Get ref seq length from max mosdepth per base BED coverage value.
* Add more conditional formatting
* Fix ``execution_report.html`` finding
* Fix version printing; add to help
* Add epilog with usage info


0.4.0 (2021-04-23)
------------------

* Adds "Variants Summary" sheet summarizing variant information across all samples
* Adds comments to AF values in "Variant Matrix" sheet
* Fixes width/height of cell comments to be based on length of comment text

0.3.0 (2021-04-23)
------------------

* Adds support for adding Ct values from a Ct values table (tab-delimited, CSV, ODS, XLSX format) into an xlavir report.

0.2.4 (2021-04-19)
------------------

* Fixes issue with SnpSift table file parsing and variable naming in variants.py (#4, #5)

0.2.3 (2021-04-19)
------------------

* Fixes issue with SnpSift table file parsing. Adds check to see if SnpSift column is dtype object/str before using .str Series methods (#4)

0.2.2 (2021-03-30)
------------------

* Fixes issue with SnpEff/SnpSift AA change parsing.

0.2.1 (2021-03-29)
------------------

* Fix division by zero error due to variants with DP values of 0

0.2.0 (2021-03-04)
------------------

* Added header comments with descriptions of field content
* Added comment to Variant Matrix sheet A1 cell describing what is shown in the matrix
* Added highlighting of samples failing QC in other sheets
* Fixed image scaling by determining image size with imageio
* Added Medaka_ / Longshot_ VCF parsing

0.1.1 (2021-02-16)
------------------

* Collect sample results from a `nf-core/viralrecon`_ or `peterk87/nf-virontus`_ into a Excel report
    * Samtools_ read mapping stats (``flagstat``)
    * Mosdepth_ read mapping coverage information
    * Variant calling information (SnpEff_ and SnpSift_ results, VCF file information)
    * Consensus sequences
* iVar VCF parsing
* QA/QC of sample analysis results (basic PASS/FAIL based on minimum genome coverage and depth)
* Nextflow workflow execution information
* Prepend worksheets from other Excel documents into the report (e.g. cover page/sheet, sample sheet, lab results)
* Add custom images into worksheets with custom names and descriptions (e.g. phylogenetic tree figure PNG)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _nf-core/viralrecon: https://github.com/nf-core/viralrecon
.. _peterk87/nf-virontus: https://github.com/peterk87/nf-virontus/
.. _Bcftools: https://www.htslib.org/doc/bcftools.html
.. _Samtools: https://samtools.github.io/
.. _SnpEff: https://pcingola.github.io/SnpEff/se_introduction/
.. _SnpSift: https://pcingola.github.io/SnpEff/ss_introduction/
.. _Mosdepth: https://github.com/brentp/mosdepth
.. _Longshot: https://github.com/pjedge/longshot
.. _Medaka: https://github.com/nanoporetech/medaka
