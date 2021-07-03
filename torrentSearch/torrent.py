#!/usr/bin/env python3.6

from json import dumps
from utils import humansize, representsInteger

RELEASE_TYPES = ('bdremux', 'brremux', 'remux',
	'bdrip', 'brrip', 'blu-ray', 'bluray', 'bdmv', 'bdr', 'bd5',
	'web-cap', 'webcap', 'web cap',
	'webrip', 'web rip', 'web-rip', 'web',
	'webdl', 'web dl', 'web-dl', 'hdrip',
	'dsr', 'dsrip', 'satrip', 'dthrip', 'dvbrip', 'hdtv', 'pdtv', 'tvrip', 'hdtvrip',
	'dvdr', 'dvd-full', 'full-rip', 'iso',
	'ts', 'hdts', 'hdts', 'telesync', 'pdvd', 'predvdrip',
	'camrip', 'cam')

class Torrent(object):
	def __init__(self, name, magnet=None, size=None, uploader=None, date=None,
		seed_count=None, leech_count=None, url=None):
		self.name  = name
		self.magnet = magnet
		self.size = size
		self.uploader = uploader
		self.date = date
		self.seed_count = seed_count
		self.leech_count = leech_count
		self.url = url

		if (size != '' and representsInteger(size)):
			self.human_size = humansize(int(size))

	def find_release_type(self):
		name = self.name.casefold()
		return [r_type for r_type in RELEASE_TYPES if r_type in name]

	def get_all_attr(self):
		return ({'name': self.name, 'magnet': self.magnet,'uploader': self.uploader,
			'size': self.size,'date': self.date,'seed': self.seed_count,
			'leech': self.leech_count, 'url': self.url, 'release_type': self.find_release_type()})

	def to_json(self):
		return dumps(self.get_all_attr())

	def __repr__(self):
		return '<%s [%r]>' % (self.__class__.__name__, self.name)