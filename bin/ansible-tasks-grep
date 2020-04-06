#! /usr/bin/env python3

import re
import sys
import json
import logging
import argparse
import subprocess

def run(cmd, stdin=None):
  if isinstance(cmd, str):
    cmd = cmd.split()
  log.info('Executing {cmd}'.format(**locals()))
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin)
  (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
  rc = p.wait()
  log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

parser = argparse.ArgumentParser(description='Search Ansible task output')
parser.add_argument('pattern', help='Regular expression with which to search')
parser.add_argument('files', metavar='file', nargs='*', help='One or more stdout files from running Ansible playbooks')
parser.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

regexp = re.compile(args.pattern, flags=re.IGNORECASE if args.ignore_case else 0)

cmd = ['bash', '-c', 'ansible-tasks {files} | table.py -i fixed -o json --strict'.format(files=' '.join(args.files))]
(rc, stdout, stderr) = run(cmd, stdin=None if args.files else sys.stdin)
if (rc == 0) and stdout:
  tasks = json.loads(stdout)
  for task in tasks:
    if regexp.search(task['Task']):
      print(json.dumps(task, sort_keys=True))
else:
  parser.error(f'{cmd} failed')
