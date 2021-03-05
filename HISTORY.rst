=======
History
=======

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
