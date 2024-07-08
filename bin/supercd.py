#! /usr/bin/env python3

import re
import os
import signal
import fnmatch
import logging
import argparse

import bruno_tools

parser = argparse.ArgumentParser(description='`Super cd` Python code')
parser.add_argument('pat', help='Glob pattern to search for')
parser.add_argument('-b', '--bash', action='store_true', help='Generate output to set bash array')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

files = bruno_tools.run(['find', os.path.expanduser('~'), '-name', args.pat], log=log)[1].splitlines()

if args.bash:
  print(f'({" ".join(files)})')
else:
  print('\n'.join(files))
