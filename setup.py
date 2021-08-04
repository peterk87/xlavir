#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'typer',
    'rich',
    'pandas',
    'numpy>=1.20.0',
    'xlsxwriter',
    'pydantic',
    'beautifulsoup4',
    'biopython',
    'openpyxl',
    'imageio',
    'odfpy',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Peter Kruczkiewicz",
    author_email='peter.kruczkiewicz@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Excel report from viral sequencing analysis output",
    entry_points={
        'console_scripts': [
            'xlavir=xlavir.cli:app',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='xlavir',
    name='xlavir',
    packages=find_packages(include=['xlavir', 'xlavir.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/peterk87/xlavir',
    version='0.5.1',
    zip_safe=False,
)
