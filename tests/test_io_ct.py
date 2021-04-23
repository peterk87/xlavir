from xlavir.io import ct
from pathlib import Path

dirpath = Path(__file__).parent


def test_parse_ct_tables():
    expected = {'Sample1': 23.0, 'Sample2': 34.8, 'Sample3': 0.0}
    io_ct_dir = dirpath / 'data/io'
    for ext in ['.ods', '.tsv', '.xlsx']:
        p = io_ct_dir / f'ct{ext}'
        assert ct.read_ct_table(p) == expected, \
            f'Should be able to parse Ct values from table with extension="{ext}". ' \
            f'Filename: {p.absolute()}'
