#! /usr/bin/env python3

import re
import sys
import logging
import argparse
import datetime
import subprocess

def run(cmd):
  if isinstance(cmd, str):
    cmd = cmd.split()
  log.info('Executing {cmd}'.format(**locals()))
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = p.communicate()
  stdout = stdout.decode('utf-8')
  stderr = stderr.decode('utf-8')
  rc = p.wait()
  log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  if (rc != 0) or stderr:
    log.error('{cmd} failed'.format(**locals()))
    sys.stdout.write(stderr)
    exit(1)
  return (rc, stdout, stderr)

def banner(s):
  lines = s.splitlines()
  width = max([len(line) for line in lines])
  print('*' * (width + 4))
  for line in lines:
    print('* {} *'.format(line.ljust(width)))
  print('*' * (width + 4))

def watch(*names):
  out = []
  for name in names:
    value = eval(name)
    if name.startswith('text'):
      value = repr(value[:20])
    out.append('{name}: {value}'.format(**locals()))
  log.info(', '.join(out)) 

def compare():
  lines = []
  lines.append('{commit1} {date1} {author1} {text}'.format(text=text1[:50], **globals()))
  lines.append('{commit2} {date2} {author2} {text}'.format(text=text2[:50], **globals()))
  banner('\n'.join(lines))

  (rc, stdout, stderr) = run('git diff {commit2} {commit1}'.format(**globals()))
  print(stdout)
  if (args.depth != None) and (depth >= args.depth):
    exit(0)

parser = argparse.ArgumentParser(description='Show diffs between git commits')
parser.add_argument('depth', type=int, nargs='?', help='Depth of commits to compare')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
# log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

if (args.depth != None) and (args.depth < 2):
  parser.error('{args.depth} is an invalid depth'.format(**locals()))

commit_regexp = re.compile('^commit\s+([0-9a-f]{40})$')
author_regexp = re.compile('^Author:\s+(.+)$')
date_regexp = re.compile('^Date:\s+([a-z]{3} [a-z]{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4})', flags=re.IGNORECASE)
text_regexp = re.compile('^\s{4}(.+)$')

"""
       1234567890123456789012345678901234567890
commit 4ad907c03af121b24b7bb1c80b8e183ad9ea94f8
Author: belscher <belscher@cisco.com>
Date:   Mon Dec 16 23:12:29 2019 -0500

    Update Jenkinsfile

"""
depth = 0

commit1 = None
author1 = None
date1 = None
text1 = ''
commit2 = None
author2 = None
date2 = None
text2 = ''

(rc, stdout, stderr) = run('git log')
for line in stdout.splitlines():
  match = commit_regexp.search(str(line))
  if match:
    if commit1:
      if commit2:
        compare()

        commit1 = commit2
        author1 = author2
        date1 = date2
        text1 = text2

        commit2 = None
        author2 = None
        date2 = None
        text2 = ''
      commit2 = match.group(1)
    else:
      commit1 = match.group(1)
    depth += 1
  else:
    match = author_regexp.search(str(line))
    if match:
      if author1:
        author2 = match.group(1)
      else:
        author1 = match.group(1)
    else:
      match = date_regexp.search(str(line))
      if match:
        timestamp = str(datetime.datetime.strptime(match.group(1), '%a %b %d %H:%M:%S %Y'))
        if date1:
          date2 = timestamp
        else:
          date1 = timestamp
      else:
        match = text_regexp.search(str(line))
        if match:
          if text1:
            text2 = (text2 + '\n' if text2 else '') + match.group(1)
          else:
            text1 = (text1 + '\n' if text1 else '') + match.group(1)

  watch('depth', 'commit1', 'author1', 'date1', 'text1', 'commit2', 'author2', 'date2', 'text2')

if commit1 and commit2:
  compare()
