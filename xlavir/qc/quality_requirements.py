from pydantic import BaseModel


class QualityRequirements(BaseModel):
    min_genome_coverage: float = 0.95
    min_median_depth: int = 30
    low_coverage_threshold: int = 10
    major_allele_freq: float = 0.75
