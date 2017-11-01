#!/usr/bin/env python3.6
import configparser

def create_jackett_client():
	config = configparser.ConfigParser()
	config.read('config.example.ini')
	jackett_host = config['JACKETT']['JACKETT_HOST']
	jackett_port = config['JACKETT']['JACKETT_PORT']
	jackett_use_ssl = config['JACKETT']['JACKETT_SSL']

	return [jackett_host, jackett_port, jackett_use_ssl]

def search(term='', user=None, sort='date', order='desc', category='0_0',
		quality_filter='0', page='1', per_page=75):
    query_args = {
        'term': term,
        'user': user,
        'sort': sort,
        'order': order,
        'category': category,
        'page': page,
        'per_page': per_page,
        'max_search_results': app.config.get('MAX_SEARCH_RESULT', 1000)
    }

    jackettResult = search_jackett(**query_args)
    return jackettResult

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
		if intersecting_release_types and int(torrent.seed_count) > 0 and float(size) > 4 and size_id == 'GiB':
			print('{} : {} : {} {}'.format(torrent.name, torrent.size, torrent.seed_count, torrent.magnet))
			interesting_torrents.append(torrent)
		# else:
		# 	print('Denied match! %s : %s : %s' % (torrent.name, torrent.size, torrent.seed_count))

	return interesting_torrents


def searchTorrentSite(query, site='piratebay'):
	if site is 'piratebay':
		pirate = piratebay()
		torrents_found = pirate.search(query, page=0, multiple_pages=5, sort='size')
	elif site is 'jackett':
		jackett = jackett()
		torrents_found = pirate.search(query)

	pprint(torrents_found)
	candidates = chooseCandidate(torrents_found)
	pprint(candidates)
	exit(0)
	torrents_found = pirate.search(query, page=0, multiple_pages=0, sort='size', category='movies')
	movie_candidates = chooseCandidate(torrents_found)

	print('Length full: {}'.format(len(candidates)))
	print('Length movies: {}'.format(len(movie_candidates)))
	# torrents_found = pirate.next_page()
	# pprint(torrents_found)
	# candidates = chooseCandidate(torrents_found)

	# Can autocall to next_page in a looped way to get more if nothing is found
	# and there is more pages to be looked at
	

def main():
	query = sys.argv[1]
	searchTorrentSite(query)

if __name__ == '__main__':
	main()