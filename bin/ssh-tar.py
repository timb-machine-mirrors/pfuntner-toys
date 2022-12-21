#! /usr/bin/env python3

import logging
import argparse
import subprocess

def run(cmd, stream=None):
  if isinstance(cmd, str):
    cmd = cmd.split()
  log.debug('Executing {cmd}'.format(**locals()))
  subprocess.Popen(cmd, stdout=stream).wait()

parser = argparse.ArgumentParser(description='Perform tar on remote systems, storing compressed archive on local system')
parser.add_argument('-b', '--become', action='store_true', help='Use sudo on remote system')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
parser.add_argument('hosts', help='Comma-delimited remote host names')
parser.add_argument('files', metavar='file', nargs='+', help='One or more remote files')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.INFO - (args.verbose or 0)*10)

log.debug(f'args: {args}')

for host in args.hosts.split(','):
  log.info(host)

  with open(f'{host}.tgz', 'w') as stream:
    run(['ssh', host] + (['sudo'] if args.become else []) + ['tar', '-czf', '-'] + args.files, stream)
