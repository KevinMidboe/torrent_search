#!/usr/bin/env python3.6

import re, logging
from bs4 import BeautifulSoup

from http_utils import convert_query_to_percent_encoded_octets, build_url, fetch_url
from utils import return_re_match
from torrent import Torrent

class Piratebay(object):
	"""docstring for Jackett"""
	def __init__(self, host, path, limit, ssl):
		super(Piratebay, self).__init__()
		self.host = host
		self.path = path
		self.page_limit = limit
		self.ssl = ssl
		self.page = 0
		self.total_pages = -1

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
		search_query = convert_query_to_percent_encoded_octets(query)
		baseUrl = 'http://' + self.host
		
		path = [self.get_path(), search_query, str(self.page)]
		url = build_url(self.ssl, baseUrl, path)

		res = fetch_url(url)

		return self.parse_raw_page_for_torrents(res.read())




	def removeHeader(self, bs4_element):
		if ('header' in bs4_element['class']):
			return bs4_element.find_next('tr')

		return bs4_element

	def has_magnet(self, href):
		return href and re.compile('magnet').search(href)

	def parse_raw_page_for_torrents(self, content):
		soup = BeautifulSoup(content, 'html.parser')
		content_searchResult = soup.body.find(id='searchResult')

		if content_searchResult is None:
			logging.info('No torrents found for the search criteria.')
			return None
		
		listElements = content_searchResult.tr
		
		torrentWrapper = self.removeHeader(listElements)

		torrents_found = []
		for torrentElement in torrentWrapper.find_all_next('td'):
			if torrentElement.find_all("div", class_='detName'):

				name = torrentElement.find('a', class_='detLink').get_text()
				url = torrentElement.find('a', class_='detLink')['href']
				magnet = torrentElement.find(href=self.has_magnet)
				
				uploader = torrentElement.find('a', class_='detDesc')				

				if uploader is None:
					uploader = torrentElement.find('i')
					
				uploader = uploader.get_text()

				info_text = torrentElement.find('font', class_='detDesc').get_text()
				
				date = return_re_match(info_text, r"(\d+\-\d+\s\d+)|(Y\-day\s\d{2}\:\d{2})")
				size = return_re_match(info_text, r"(\d+(\.\d+)?\s[a-zA-Z]+)")

				# COULD NOT FIND HREF!
				if (magnet is None):
					continue

				seed_and_leech = torrentElement.find_all_next(attrs={"align": "right"})
				seed = seed_and_leech[0].get_text()
				leech = seed_and_leech[1].get_text()

				torrent = Torrent(name, magnet['href'], size, uploader, date, seed, leech, url)

				torrents_found.append(torrent)
			else:
				# print(torrentElement)
				continue

		logging.info('Found %s torrents for given search criteria.' % len(torrents_found))
		return torrents_found
