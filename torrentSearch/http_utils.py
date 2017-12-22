#!/usr/bin/env python3.6

import logging
import sys

from urllib import parse, request
from urllib.error import URLError

logger = logging.getLogger('torrentSearch')

def build_url(ssl, baseUrl, path, args_dict=[]):
   url_parts = list(parse.urlparse(baseUrl))
   url_parts[0] = 'https' if ssl else 'http'
   if type(path) is list:
      url_parts[2] = '/'.join(path)
   else:
      url_parts[2] = path
   url_parts[4] = parse.urlencode(args_dict)
   return parse.urlunparse(url_parts)

# Converts a input string or list to percent-encoded string,
# this is for encoding information in a Uniform Resource
# Identifier (URI) using urllib
def convert_query_to_percent_encoded_octets(input_query):
   if type(input_query) is list:
      input_query = ' '.join(input_query)

   return parse.quote(input_query)

def fetch_url(url):
   logger.debug('Fetching query: {}'.format(url))
   req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   try:
       response = request.urlopen(req, timeout=10)
       return response
   except URLError as e:
      if hasattr(e, 'reason'):
         logger.error('We failed to reach a server with request: %s' % req.full_url)
         logger.error('Reason: %s' % e.reason)
      elif hasattr(e, 'code'):
         logger.error('The server couldn\'t fulfill the request.')
         logger.error('Error code: ', e.code)
      sys.exit()
