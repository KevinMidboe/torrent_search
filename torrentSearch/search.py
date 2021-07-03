#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

import json
import logging
import logging.config

from jackett import Jackett
from piratebay import Piratebay
from utils import ColorizeFilter, getConfig

from pprint import pprint

logger = logging.getLogger('torrentSearch')

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


def searchTorrentSite(query, site='jackett', filter=None, print_result=False, config=None):
   """
   Selects site based on input and finds torrents for that site based on query

   :param configparser.ConfigParser config: integer of size of torrent filest
   :param str query: query to search search torrents for
   :param str site: the site we want to index/scrape
   :param boolean print_result: if the in results should be printed to terminal
   :return: json list with results
   :rtype: str
   """
   if config is None:
      config = getConfig()
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
