# Should maybe not be able to set values without checking if they are valid?
class piratebay(object):
	def __init__(self, query=None, page=0, sort=None, category=None):
		# This should be moved to a config file
		self.url = 'https://thepiratebay.org/search'
		self.sortTypes = {
			'size': 5,
			'seed_count': 99
		}
		self.categoryTypes = {
			'movies': 207,
			'porn_movies': 505,
		}
		# - - -

		# Req params
		self.query = query
		self.page = page
		self.sort = sort
		self.category = category
		self.total_pages = 0
		self.headers = {'User-Agent': 'Mozilla/5.0'}
		# self.headers = {}

	def build_URL_request(self):
		url = '/'.join([self.url, parse.quote(self.query), str(self.page), str(self.sort), str(self.category)])
		return request.Request(url, headers=self.headers)

	def next_page(self):
		# If page exceeds the max_page, return None
		# Can either save the last query/url in the object or have it passed 
		# again on call to next_page

		# Throw a error if it is not possible (overflow)
		self.page += 1
		print(self.page)
		raw_page = self.callPirateBaT()
		return self.parse_raw_page_for_torrents(raw_page)

	def set_total_pages(self, raw_page):
		# body-id:searchResults-id:content-align:center
		soup = BeautifulSoup(raw_page, 'html.parser')
		content_searchResult = soup.body.find(id='SearchResults')
		page_div = content_searchResult.find_next(attrs={"align": "center"})

		last_page = 0
		for page in page_div.find_all('a'):
			last_page += 1

		self.total_pages = last_page

	def callPirateBaT(self):
		req = self.build_URL_request()
			
		raw_page = self.fetchURL(req).read()
		logging.info('Finished searching piratebay for query | %s' % stringTime())

		if raw_page is None:
			raise ValueError('Search result returned no content. Please check log for error reason.')

		if self.total_pages is 0:
			self.set_total_pages(raw_page)
		
		return raw_page


	# Sets the search
	def search(self, query, multiple_pages=1, page=0, sort=None, category=None):
		# This should not be logged here, but in loop. Something else here maybe?
		logging.info('Searching piratebay with query: %r, sort: %s and category: %s | %s' % 
			(query, sort, category, stringTime()))
		
		if sort is not None and sort in self.sortTypes:
			self.sort = self.sortTypes[sort]
		else:
			raise ValueError('Invalid sort category for piratebay search')

		# Verify input? and reset total_pages
		self.query = query

		self.total_pages = 0
		
		if str(page).isnumeric() and type(page) == int and page >= 0:
			self.page = page
		
		# TODO add category list
		if category is not None and category in self.categoryTypes:
			self.category = self.categoryTypes[category]

		# TODO Pull most of this logic out bc it needs to also be done in next_page
		
		raw_page = self.callPirateBaT()
		torrents_found = self.parse_raw_page_for_torrents(raw_page)
		print(self.page)
		
		# Fetch in parallel
		n = pagesToCount(multiple_pages, self.total_pages)
		while n > 1:
			torrents_found.extend(self.next_page())
			n -= 1

		return torrents_found


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

		
	def fetchURL(self, req):
		try:
		    response = request.urlopen(req)
		except URLError as e:
		    if hasattr(e, 'reason'):
		        logging.error('We failed to reach a server with request: %s' % req.full_url)
		        logging.error('Reason: %s' % e.reason)
		    elif hasattr(e, 'code'):
		        logging.error('The server couldn\'t fulfill the request.')
		        logging.error('Error code: ', e.code)
		else:
		    return response