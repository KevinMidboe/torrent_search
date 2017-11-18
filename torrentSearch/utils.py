#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-11-01 15:57:23
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-11-19 00:05:10

import re
from datetime import datetime

SYMBOLS = {
	'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
	'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
					   'zetta', 'iotta'),
	'iec'           : ('BiB', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'),
	'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
					   'zebi', 'yobi'),
}

def sanitize(string, ignore_characters=None, replace_characters=None):
	"""Sanitize a string to strip special characters.

	:param str string: the string to sanitize.
	:param set ignore_characters: characters to ignore.
	:return: the sanitized string.
	:rtype: str

	"""
	# only deal with strings
	if string is None:
		return
	
	replace_characters = replace_characters or ''

	ignore_characters = ignore_characters or set()

	characters = ignore_characters
	if characters:
		string = re.sub(r'[%s]' % re.escape(''.join(characters)), replace_characters, string)

	return string

def return_re_match(string, re_statement):
	if string is None:
		return

	m = re.search(re_statement, string)
	if 'Y-day' in m.group():
		return datetime.now().strftime('%m-%d %Y')
	return sanitize(m.group(), '\xa0', ' ')


# Can maybe be moved away from this class
# returns a number that is either the value of multiple_pages
# or if it exceeds total_pages, return total_pages.
def pagesToCount(multiple, total):
	if (multiple > total):
		return total
	return multiple

def deHumansize(s):
	""" 
	Attempts to guess the string format based on default symbols
	set and return the corresponding bytes as an integer.
	When unable to recognize the format ValueError is raised.

	:param str s: human file size that we want to convert
	:return: the guessed bytes in from the human file size
	:rtype: int
	"""

	init = s
	num = ""
	while s and s[0:1].isdigit() or s[0:1] == '.':
		num += s[0]
		s = s[1:]
	num = float(num)
	letter = s.strip()
	for name, sset in SYMBOLS.items():
		if letter in sset:
			break
	else:
		if letter == 'k':
			# treat 'k' as an alias for 'K' as per: http://goo.gl/kTQMs
			sset = SYMBOLS['customary']
			letter = letter.upper()
		else:
			raise ValueError("can't interpret %r" % init)
	prefix = {sset[0]:1}
	for i, s in enumerate(sset[1:]):
		prefix[s] = 1 << (i+1)*10
	return int(num * prefix[letter])

def humansize(nbytes):
	suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	i = 0
	while nbytes >= 1024 and i < len(suffixes)-1:
		nbytes /= 1024.
		i += 1
	f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
	return '{} {}'.format(f, suffixes[i])