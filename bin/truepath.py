#! /usr/bin/env python

import os
import re
import sys
import logging
import argparse

def process(rawpath, log):
  if rawpath.startswith('-'):
    log.debug('{rawpath!r} looks like an option so I\'m going to leave it alone!'.format(**locals()))
    path = rawpath
  else:
    path = os.path.abspath(rawpath)
    log.debug('path: {path!r}'.format(**locals()))
    if 'win' in sys.platform:
      log.debug('Sorry to see you\'re using Windoze...')
      match = re.search('^/+cygdrive/+([a-z])/+(.+)$', path, flags=re.IGNORECASE)
      if match:
        path = '{drive}:/{remain}'.format(
          drive=match.group(1),
          remain=match.group(2),
        )
      else:
        path = 'C:\\cygwin64' + path.replace('/', '\\')
    else:
      log.debug('You are not using Windoze like a boss!')
  log.debug('{rawpath!r} => {path!r}'.format(**locals()))
  return path

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Get `true` path - useful on Windoze')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  parser.add_argument('paths', metavar='path', nargs='+', help='One or more paths')
  args = parser.parse_args()
  
  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
  
  for path in args.paths:
    print process(path, log)
