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
import argparse
import json
import os
import logging
import logging.config
import configparser
import signal

from docopt import docopt

from torrentSearch import __version__
from torrentSearch.jackett import Jackett
from torrentSearch.piratebay import Piratebay
from torrentSearch.utils import ColorizeFilter

from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

   searchTorrentSite(config, arguments['<query>'], site, arguments['-f'], arguments['--print'])


def getConfig():
   """
   Read path and get configuartion file with site settings

   :return: config settings read from 'config.ini'
   :rtype: configparser.ConfigParser
   """
   config = configparser.ConfigParser()
   config_dir = os.path.join(BASE_DIR, 'config.ini')
   config.read(config_dir)

   return config

def createJSONList(torrents):
   """
   Iterates over all torrent objects in torrents and gets all attributes which are appended to a list

   :param list torrents: integer of size of torrent file
   :return: List of torrents with all their info in a JSON format
   :rtype: str
   """
   jsonList = []
   for torrent in torrents:
      jsonList.append(torrent.get_all_attr())

   return json.dumps(jsonList)

# This should be done front_end!
# I.E. filtering like this should be done in another script
# and should be done with the shared standard for types. 
# PS: Is it the right move to use a shared standard? What
# happens if it is no longer public?
def chooseCandidate(torrent_list):
   """
   Takes a list of torrents and filtes then on a given release type
   Returns: JSON list of torrents only matching release type
   """
   interesting_torrents = []
   match_release_type = ['bdremux', 'brremux', 'remux', 'bdrip', 'brrip', 'blu-ray', 'bluray', 'bdmv', 'bdr', 'bd5']

   for torrent in torrent_list:
      intersecting_release_types = set(torrent.find_release_type()) & set(match_release_type)

      size, _, size_id = torrent.size.partition(' ')
      if intersecting_release_types:
         interesting_torrents.append(torrent)   

   return interesting_torrents


def searchTorrentSite(config, query, site, filter, print_result):
   """
   Selects site based on input and finds torrents for that site based on query

   :param configparser.ConfigParser config: integer of size of torrent filest
   :param str query: query to search search torrents for
   :param str site: the site we want to index/scrape
   :param boolean print_result: if the in results should be printed to terminal
   :return: json list with results
   :rtype: str
   """
   logger.debug('Searching for query {} at {}'.format(query, site))

   if site == 'piratebay':
      pirate = Piratebay(config['PIRATEBAY']['HOST'], config['PIRATEBAY']['PATH'],
         config['PIRATEBAY']['LIMIT'], config['PIRATEBAY']['SSL'])
      torrents_found = pirate.search(query)
   elif site == 'jackett':
      jackett = Jackett(config['JACKETT']['APIKEY'], config['JACKETT']['HOST'], 
         config['JACKETT']['PATH'], config['JACKETT']['LIMIT'], config.getboolean('JACKETT', 'SSL'))
      torrents_found = jackett.search(query)

   if (filter):
      torrents_found = chooseCandidate(torrents_found)
   
   jsonList = createJSONList(torrents_found)

   if (print_result):
      print(jsonList)

   return jsonList

def signal_handler(signal, frame):
   """
   Handle exit by Keyboardinterrupt
   """
   logger.info('\nGood bye!')
   sys.exit(0)

if __name__ == '__main__':
   main()
