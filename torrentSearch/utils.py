#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-11-01 15:57:23
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-12-22 12:07:18

import re
import os
import logging
import colored
import configparser

from datetime import datetime
from colored import stylize

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOLS = {
   'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
   'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
      'zetta', 'iotta'),
   'iec'           : ('BiB', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'),
   'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
      'zebi', 'yobi'),
}

__all__ = ('ColorizeFilter', )

def getConfig():
   """
   Read path and get configuartion file with site settings

   :return: config settings read from 'config.ini'
   :rtype: configparser.ConfigParser
   """
   config = configparser.ConfigParser()
   config_dir = os.path.join(BASE_DIR, 'config.ini')
   config.read(config_dir)

   return config

class ColorizeFilter(logging.Filter):
   """
   Class for setting specific colors to levels of severity for log output
   """

   color_by_level = {
      logging.DEBUG: 'yellow',
      logging.WARNING: 'red',
      logging.ERROR: 'red',
      logging.INFO: 'white'
   }

   def filter(self, record):
      record.raw_msg = record.msg
      color = self.color_by_level.get(record.levelno)
      if color:
         record.msg = stylize(record.msg, colored.fg(color))
      return True

def sanitize(string, ignore_characters=None, replace_characters=None):
   """
   Sanitize a string to strip special characters.

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
   """
   Helper function for checking if a string contains a given regex statement

   :param str string, str re_statement: string we want to check and regex string we 
      check for in string
   :return: sanitized string of the match we found
   :rtype: str
   """
   if string is None:
      return

   m = re.search(re_statement, string)
   # This is here for a edge case for piratebay torrent dates
   if 'Y-day' in m.group():
      return datetime.now().strftime('%m-%d %Y')
   return sanitize(m.group(), '\xa0', ' ')

def representsInteger(str):
   """
   Checks if a string only contains integers

   :param str str: string we want to check only has integers
   :return: if string only contains integers
   :rtype: boolean
   """
   try:
      int(str)
      return True
   except ValueError:
      return False

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
   """ 
   Translates a size in bytes to a human readable size format

   :param int nbytes: integer of size of torrent file
   :return: size in bytes in a human readable format
   :rtype: str
   """
   suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
   i = 0
   while nbytes >= 1024 and i < len(suffixes)-1:
      nbytes /= 1024.
      i += 1
   f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
   return '{} {}'.format(f, suffixes[i])

