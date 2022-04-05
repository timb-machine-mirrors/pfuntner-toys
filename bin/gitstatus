#! /usr/bin/env python3

import re
import sys
import logging
import argparse
import subprocess

def see(expression):
  log.info('>>> {expression}: {value}'.format(expression=expression, value=eval(expression)))

parser = argparse.ArgumentParser(description='Simplify `git status` output')
parser.add_argument('-c', '--changes', '--changed', '--modified', dest='changes', action='store_true', help='Show changed files')
parser.add_argument('-u', '--untracked', dest='untracked', action='store_true', help='Show untracked files')
parser.add_argument('--unmerged', dest='unmerged', action='store_true', help='Show unmerged files')
parser.add_argument('-a', '--all', dest='all', action='store_true', help='Show changed, unmerged, and untracked files')
parser.add_argument('-v', '--verbose', dest='verbose', action='count', help='Enable debugging')
parser.add_argument('files', metavar='file', nargs='*', help='Files to pass to `git status`')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

section_regexps = {
  'modified': {
     'header': re.compile('^#?\s*Changes not staged for commit:'),
     'file': re.compile('^#?\s+modified:\s+(.*)$'),
     'requested': False,
  },
  'unmerged': {
     'header': re.compile('^#?\s*Unmerged paths:'),
     'file': re.compile('^#?\s+both modified:\s+(.*)$'),
     'requested': False,
  },
  'untracked': {
     'header': re.compile('^#?\s*Untracked files:'),
     'file': re.compile('^#?\t([^( ].*)$'),
     'requested': False,
  },
}

if args.changes or args.all:
  section_regexps['modified']['requested'] = not section_regexps['modified']['requested']
if args.untracked or args.all:
  section_regexps['untracked']['requested'] = not section_regexps['untracked']['requested']
if args.unmerged or args.all:
  section_regexps['unmerged']['requested'] = not section_regexps['unmerged']['requested']

if not any([section_regexps[section]['requested'] for section in section_regexps.keys()]):
  section_regexps['modified']['requested'] = True # default to modified only

see('section_regexps')

cmd = ['git', 'status'] + args.files
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout, stderr) = p.communicate()
stdout = stdout.decode('utf-8')
stderr = stderr.decode('utf-8')
rc = p.wait()
if (rc != 0) or stderr:
  log.critical('{cmd} failed: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  exit(1)

section_end_regexp = re.compile('^(|# )[A-Za-z]')

inside = None

items = 0

for line in stdout.splitlines():
  if section_end_regexp.search(str(line)):
    inside = None
    for section in section_regexps.keys():
      if section_regexps[section]['header'].search(str(line)):
        inside = section

  see('(line, inside)')

  if section_regexps['modified']['requested'] and (inside == 'modified'):
    match = section_regexps['modified']['file'].search(str(line))
    if match:
      print(match.group(1))
      items += 1

  if section_regexps['untracked']['requested'] and (inside == 'untracked'):
    match = section_regexps['untracked']['file'].search(str(line))
    if match:
      print(match.group(1))
      items += 1

  if section_regexps['unmerged']['requested'] and (inside == 'unmerged'):
    match = section_regexps['unmerged']['file'].search(str(line))
    if match:
      print(match.group(1))
      items += 1

if not items:
  log.warning('No files changed')
  exit(1)
