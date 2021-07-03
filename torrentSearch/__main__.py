#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

"""Torrent Search.

Usage:
   search.py <query> [-s <site>] [-f] [-p | --print] [--debug | --warning | --error]
   search.py (-h | --help)
   search.py --version

Options:
   -h --help     Show this screen
   -s [site]     Site to index [default: piratebay] (piratebay|jackett)
   -p --print    Print result to console
   -f            Filter response on release type
   --version     Show version
   --debug       Print all debug logs
   --warning     Print only logged warnings
   --error       Print error messages (Error/Warning)
"""

import sys
import logging
import logging.config
import signal

from docopt import docopt
from __init__ import __version__

from search import searchTorrentSite
from utils import ColorizeFilter, getConfig

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)8s %(name)s | %(message)s')
ch.setFormatter(formatter)

logger = logging.getLogger('torrentSearch')
logger.addHandler(ch)
logger.setLevel(logging.ERROR)  # This toggles all the logging in your app
logger.addFilter(ColorizeFilter())

def main():
   """
   Main function, call searchTorrentSite
   """
   signal.signal(signal.SIGINT, signal_handler)

   arguments = docopt(__doc__, version=__version__)

   if arguments['--debug']:
      logger.level = logging.DEBUG
   elif arguments['--warning']:
      logger.level = logging.WARNING
   elif arguments['--error']:
      logger.level = logging.ERROR

   logger.info('Torrent Searcher')
   logger.debug(arguments)

   # Fetch config
   config = getConfig()

   if arguments['-s'] in config['DEFAULT']['SITE_OPTIONS'].split(','):
      site = arguments['-s']
      logger.debug('site selected: {}'.format(site))
   else:
      logger.error('"{}" is a invalid site. Select from: {}'.format(arguments['-s'], config['DEFAULT']['SITE_OPTIONS']))
      sys.exit()

   searchTorrentSite(arguments['<query>'], site, arguments['-f'], arguments['--print'], config)

def signal_handler(signal, frame):
   """
   Handle exit by Keyboardinterrupt
   """
   logger.info('\nGood bye!')
   sys.exit(0)

if __name__ == '__main__':
   main()
