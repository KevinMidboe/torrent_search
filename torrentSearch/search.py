#!/usr/bin/env python3.6
import configparser
import sys, argparse, json, os

from jackett import Jackett
from piratebay import Piratebay

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getConfig():
	config = configparser.ConfigParser()
	config_dir = os.path.join(BASE_DIR, 'config.example.ini')
	config.read(config_dir)
	jackett_host = config['JACKETT']['HOST']
	jackett_use_ssl = config['JACKETT']['SSL']

	return config


# This should be done front_end!
# I.E. filtering like this should be done in another script
# and should be done with the shared standard for types. 
# PS: Is it the right move to use a shared standard? What
# happens if it is no longer public?
def chooseCandidate(torrent_list):
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
		# 	print('Denied match! %s : %s : %s' % (torrent.name, torrent.size, torrent.seed_count))

	return interesting_torrents


def searchTorrentSite(config, query, site):
	if site == 'piratebay':
		pirate = Piratebay(config['PIRATEBAY']['HOST'], config['PIRATEBAY']['PATH'],
			config['PIRATEBAY']['LIMIT'], config['PIRATEBAY']['SSL'])
		torrents_found = pirate.search(query)
	elif site == 'jackett':
		jackett = Jackett(config['JACKETT']['APIKEY'], config['JACKETT']['HOST'], 
			config['JACKETT']['PATH'], config['JACKETT']['LIMIT'], config.getboolean('JACKETT', 'SSL'))
		torrents_found = jackett.search(query)

	# print(json.dumps(torrents_found))
	# exit(0)

	candidates = chooseCandidate(torrents_found)
	print(json.dumps(candidates))

	# print('Length full: {}'.format(len(candidates)))
	# print('Length movies: {}'.format(len(movie_candidates)))
	# torrents_found = pirate.next_page()
	# pprint(torrents_found)
	# candidates = chooseCandidate(torrents_found)

	# Can autocall to next_page in a looped way to get more if nothing is found
	# and there is more pages to be looked at
	

def main():
	site_options = ['jackett', 'piratebay']
	parser = argparse.ArgumentParser(prog='Torrent Search', description='Search different torrent sites by query.')
	parser.add_argument('query', 
		nargs='+', 
		help='query for searching torrents.')
	parser.add_argument('-s', '--site', 
		nargs='?', 
		default='jackett', 
		const='jackett', 
		type=str,
		choices=site_options,
		help='the site to index (default: %(default)s)')
	parser.add_argument('-v', 
		action='store_true', 
		help='verbose output.')

	args = parser.parse_args()

	config = getConfig()
	searchTorrentSite(config, args.query, args.site)

if __name__ == '__main__':
	main()
