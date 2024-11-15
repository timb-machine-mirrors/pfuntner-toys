#! /usr/bin/env python3

import os
import sys
import glob
import signal
import logging
import argparse

parser = argparse.ArgumentParser(description='Find virtual environment activation script')
parser.add_argument('dir', nargs='?', help='Directory in which to look.  Defaults to ./venv/bin/activate and ../venv/bin/activate')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger(sys.argv[0])
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

if args.dir:
  paths = [
    os.path.join(args.dir, 'venv/bin/activate'),
    os.path.join(args.dir, 'bin/activate'),
  ]
else:
  paths = [
    'venv/bin/activate',
    'bin/activate',
  ]

for path in paths:
  log.info(f'Testing {path=}')
  if os.path.isfile(path):
    print(path)
    exit(0)

log.warning(f'Could not find: {paths}')
print('/dev/null')
