#! /usr/bin/env python3

import re
import os
import signal
import logging
import argparse
import subprocess

def run(cmd, stdin=None, capture=True, shell=False):
  if shell:
    if isinstance(cmd, list):
      cmd = ' '.join(cmd)
  elif isinstance(cmd, str):
    cmd = cmd.split()

  log.info('Executing {cmd}'.format(**locals()))

  p = None
  try:
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE if stdin else None, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None, shell=shell)
  except Exception as e:
    (rc, stdout, stderr) = (-1, '', f'Caught {e!s} running {cmd!r}')

  if p:
    if stdin:
      p.stdin.write(stdin.encode())
    if capture:
      (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
    else:
      (stdout, stderr) = ('', '')
    rc = p.wait()

  log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

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
(rc, stdout, stderr) = run(f'find {os.path.expanduser("~")} -follow -type d ! -path */.* ! -path */Downloads* ! -path */third-party* ! -path */venv/* ! -path */__pycache__*')
files = list()
for file in stdout.splitlines():
  if regexp.search(os.path.basename(file)):
    files.append(protect_metachars(file) if args.bash else file)

if args.bash:
  print(f'({" ".join(files)})')
else:
  print('\n'.join(files))
