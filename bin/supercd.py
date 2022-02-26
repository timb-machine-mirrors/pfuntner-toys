#! /usr/bin/env python3

import re
import os
import signal
import logging
import argparse

def dive(path):
  ret = list()

  if not ('/.' in path or '/Downloads' in path or '/third-party' in path or '/__pycache__' in path):

    if regexp.search(os.path.basename(path)) and os.path.isdir(path) and not os.path.islink(path):
      ret.append(path)
  
    if os.path.isdir(path):
      children = list()
      try:
        children = os.listdir(path)
      except Exception as e:
        log.info(f'listdir({path!r}) error: {e!r}')
      for filename in children:
        ret += dive(os.path.join(path, filename))

  return ret

def protect_metachars(s):
  ret = ''
  for c in s:
    if c in '"$':
      ret += '\\'
    ret += c
  return f'"{ret}"'

parser = argparse.ArgumentParser(description='`Super cd` Python code')
parser.add_argument('pat', help='Pattern to search for')
parser.add_argument('-b', '--bash', action='store_true', help='Generate output to set bash array')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

regexp = re.compile(args.pat)
files = dive(os.path.expanduser("~"))

if args.bash:
  print(f'({" ".join(files)})')
else:
  print('\n'.join(files))
