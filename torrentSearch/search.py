#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

"""Torrent Search.

Usage:
   search.py <query> [-s <site>] [-p | --print] [--debug | --warning | --error]
   search.py (-h | --help)
   search.py --version

Options:
   -h --help     Show this screen
   -s [site]     Site to index [default: piratebay] (piratebay|jackett)
   -p --print    Print result to console
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
from jackett import Jackett
from torrentSearch.piratebay import Piratebay
from torrentSearch.utils import ColorizeFilter

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

   searchTorrentSite(config, arguments['<query>'], site, arguments['--print'])


def getConfig():
   """
   Read path and get configuartion file with site settings
   Returns config [configparser]
   """
   config = configparser.ConfigParser()
   config_dir = os.path.join(BASE_DIR, 'config.ini')
   config.read(config_dir)

   return config

def createJSONList(torrents):
   """
   Iterates over all torrent objects in torrents and gets all attributes which are appended to a list
   Returns: List of torrents with all their info in a JSON format
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
      # if intersecting_release_types and int(torrent.seed_count) > 0 and float(size) > 4 and size_id == 'GiB':
      if intersecting_release_types:
         interesting_torrents.append(torrent.get_all_attr())   
         # print('{} : {} : {} {}'.format(torrent.name, torrent.size, torrent.seed_count, torrent.magnet))
         # interesting_torrents.append(torrent)
      # else:
      #  print('Denied match! %s : %s : %s' % (torrent.name, torrent.size, torrent.seed_count))

   return interesting_torrents


def searchTorrentSite(config, query, site, print_result):
   """
   Selects site based on input and finds torrents for that site based on query
   Returns json list with results. If print_results is True in args then also prints the output to terminal
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
