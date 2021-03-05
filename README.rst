======
xlavir
======


.. image:: https://img.shields.io/pypi/v/xlavir.svg
        :target: https://pypi.python.org/pypi/xlavir

.. image:: https://github.com/peterk87/xlavir/workflows/CI/badge.svg?branch=master
        :target: https://github.com/peterk87/xlavir/actions

.. image:: https://readthedocs.org/projects/xlavir/badge/?version=latest
        :target: https://xlavir.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Excel report from viral sequencing data analysis output from the `nf-core/viralrecon`_ or `peterk87/nf-virontus`_ Nextflow pipelines.


* Free software: MIT license
* Documentation: https://xlavir.readthedocs.io.


Features
--------

* Collect sample results from a `nf-core/viralrecon`_ or `peterk87/nf-virontus`_ into a Excel report
    * Samtools_ read mapping stats (``flagstat``)
    * Mosdepth_ read mapping coverage information
    * Variant calling information (SnpEff_ and SnpSift_ results, VCF file information)
    * Consensus sequences
* QA/QC of sample analysis results (basic PASS/FAIL based on minimum genome coverage and depth)
* Nextflow workflow execution information
* Prepend worksheets from other Excel documents into the report (e.g. cover page/sheet, sample sheet, lab results)
* Add custom images into worksheets with custom names and descriptions (e.g. phylogenetic tree figure PNG)

Roadmap
-------

* Bcftools_ variant calling stats sheet
* Sample metadata table to merge with certain stats?
* YAML config to info sheet?
* coverage chart with controls?

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _nf-core/viralrecon: https://github.com/nf-core/viralrecon
.. _peterk87/nf-virontus: https://github.com/peterk87/nf-virontus/
.. _Bcftools: https://www.htslib.org/doc/bcftools.html
.. _Samtools: https://samtools.github.io/
.. _SnpEff: https://pcingola.github.io/SnpEff/se_introduction/
.. _SnpSift: https://pcingola.github.io/SnpEff/ss_introduction/
.. _Mosdepth: https://github.com/brentp/mosdepth
