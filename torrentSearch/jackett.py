#!/usr/bin/env python3.6

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring

from http_utils import convert_query_to_percent_encoded_octets, build_url, fetch_url
from torrent import Torrent
from utils import humansize

class Jackett(object):
	"""docstring for Jackett"""
	def __init__(self, apikey, host, path, limit, ssl):
		super(Jackett, self).__init__()
		self.apikey = apikey
		self.host = host
		self.path = path
		self.page_limit = limit
		self.ssl = ssl

	# Returns the api key set in the initiator
	# return [string]
	def get_apikey(self):
		return self.apikey

	# Returns the path set in the initiator
	# return [string]
	def get_path(self):
		return self.path

	# Returns the page_limit set in the initiator
	# return [string]
	def get_page_limit(self):
		return self.page_limit

	# Starts the call to getting result from our indexer
	# query [string]
	# returns [List of Torrent objects]
	def search(self, query):
		baseUrl = 'http://' + self.host
		path = self.get_path()
		args_dict = {
			'apikey': self.get_apikey(),
			'limit': self.get_page_limit(),
			'q': convert_query_to_percent_encoded_octets(query)
		}

		url = build_url(self.ssl, baseUrl, path, args_dict)

		res = fetch_url(url)

		return self.parse_xml_for_torrents(res.read())


	# def __init__(self, name, magnet=None, size=None, uploader=None, date=None,
	# 	seed_count=None, leech_count=None, url=None):

	def parse_xml_for_torrents(self, raw_xml):
		tree = ET.fromstring(raw_xml)
		channel = tree.find('channel')
		results = []
		for child in channel.findall('item'):
			title = child.find('title').text
			date = child.find('pubDate').text
			magnet = child.find('link').text
			size = child.find('size').text
			size = humansize(int(size))

			torrent = Torrent(title, magnet=magnet, size=size, date=date)
			results.append(torrent)

		return results

