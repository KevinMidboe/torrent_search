
class Jackett(object):
	"""docstring for Jackett"""
	def __init__(self, url, query, apikey, limit):
		super(Jackett, self).__init__()
		self.url = url
		self.query = query
		self.apikey = apikey
		self.limit = limit

	@classmethod
	def build_search_url(url, query, apikey, limit):
        return cls(url, query, apikey, limit)