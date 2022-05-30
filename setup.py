#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
from sys import path
from os.path import dirname

from torrentSearch.__version__ import __version__

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name='torrentSearch',
    version=__version__,
    packages=find_packages(),
    package_data={
        'torrentSearch': ['default_config.ini'],
    },
    author='KevinMidboe',
    description='Search For Torrents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'bs4',
        'docopt',
	    'colored'
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
