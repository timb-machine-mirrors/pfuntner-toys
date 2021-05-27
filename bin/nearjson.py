#! /usr/bin/env python3

import re
import sys
import json
import signal
import logging
import argparse

parser = argparse.ArgumentParser(description='Process a JSON dict from a line of text')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

if sys.stdin.isatty():
  parser.error('stdin must be redirected')

regexp = re.compile(r'^[^{]*({.+})[^}]*$')

for (pos, line) in enumerate(sys.stdin.read().splitlines()):
  match = regexp.search(line)
  if match:
    log.debug(f'line {pos} has a dict: {line!r}')
    data = match.group(1)
    log.info(f'{pos}: {data!r}')
    try:
      struct = json.loads(data)
      print(json.dumps(struct))
    except Exception as e:
      log.debug(f'Could not parse as JSON: {e!s}')
  else:
    log.debug(f'line {pos} does not have a dict: {line!r}')
