from pathlib import Path

import pandas as pd

from xlavir.qc import QualityRequirements
from xlavir.tools import variants

clair3_basedir = Path('tests/data/vcfs/clair3')
bcftools_basedir = Path('tests/data/vcfs/bcftools')
ivar_basedir = Path('tests/data/vcfs/ivar')
expected_columns = [
    'sample', 'CHROM', 'POS', 'REF', 'ALT', 'REF_DP', 'ALT_DP', 'DP', 'ALT_FREQ'
]


def test_parse_clair3_vcf():
    clair3_variants = variants.get_info(basedir=clair3_basedir, qc_reqs=QualityRequirements())
    assert 'Sample1' in clair3_variants
    assert isinstance(clair3_variants['Sample1'], pd.DataFrame)
    assert clair3_variants['Sample1'].shape == (150, 9)
    assert clair3_variants['Sample1'].columns.tolist() == expected_columns


def test_parse_bcftools_vcf():
    bcftools_variants = variants.get_info(basedir=bcftools_basedir, qc_reqs=QualityRequirements())
    assert 'Sample1' in bcftools_variants
    assert isinstance(bcftools_variants['Sample1'], pd.DataFrame)
    assert bcftools_variants['Sample1'].shape == (70, 9)
    assert bcftools_variants['Sample1'].columns.tolist() == expected_columns


def test_parse_ivar_vcf():
    ivar_variants = variants.get_info(basedir=ivar_basedir, qc_reqs=QualityRequirements())
    assert 'Sample1' in ivar_variants
    assert isinstance(ivar_variants['Sample1'], pd.DataFrame)
    assert ivar_variants['Sample1'].shape == (78, 9)
    assert ivar_variants['Sample1'].columns.tolist() == expected_columns
