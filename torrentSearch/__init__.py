#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

"""Python Torrent Searcher/Scraper."""

from sys import path
from os.path import dirname
path.append(dirname(__file__))

__version__ = '0.2'

import logging
from utils import ColorizeFilter
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)8s %(name)s | %(message)s')
ch.setFormatter(formatter)

logger = logging.getLogger('torrentSearch')
logger.addHandler(ch)
logger.setLevel(logging.ERROR)  # This toggles all the logging in your app
logger.addFilter(ColorizeFilter())
