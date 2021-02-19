import re

from pydantic import BaseModel

BCFTOOLS_STATS_GLOB_PATTERNS = [
    '**/ivar/**/*AF0.*.bcftools_stats.txt',
    '**/ivar/**/*.bcftools_stats.txt',
    '**/*AF0.*.bcftools_stats.txt',
    '**/*.bcftools_stats.txt',
]

BCFTOOLS_STATS_SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.AF0\.\d+\.bcftools_stats.txt$')
]


class VariantStats(BaseModel):
    sample: str
    n_snp: int
    n_mnp: int
    n_indel: int
