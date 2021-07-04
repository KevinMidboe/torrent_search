#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
from sys import path
from os.path import dirname

import torrentSearch

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name='torrentSearch',
    version=torrentSearch.__version__,
    packages=find_packages(),
    package_data={
        'torrentSearch': ['default_config.ini'],
    },
    author='KevinMidboe',
    description='Search For Torrents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'docopt',
        'beautifulsoup4',
        'termcolor',
	    'colored',
    ],
    url='https://github.com/KevinMidboe/torrent_search',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'torrentsearch = torrentSearch.__main__:main',
        ],
    },
)
