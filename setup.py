#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import torrentSearch

setup(
    name='torrentSearch',
    version=torrentSearch.__version__,
    packages=find_packages(),
    author='KevinMidboe',
    description='Search For Torrents',
    long_description="README on github : https://github.com/KevinMidboe/torrent_search",
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
