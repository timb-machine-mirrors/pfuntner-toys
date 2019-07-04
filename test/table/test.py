#! /usr/bin/env python

import os
import re
import sys
import logging
import argparse
import subprocess

def run(cmd, stdin=None):
  if isinstance(cmd, basestring):
    cmd = cmd.split()
  p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = p.communicate(stdin or '')
  rc = p.wait()
  log.debug('{cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

parser = argparse.ArgumentParser(description='Test table script')
parser.add_argument('-c', '--create', dest='create', action='store_true', help='Create output')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

test_dir = os.path.dirname(sys.argv[0])
table_script = os.path.join(test_dir, '..', '..', 'bin', 'table.py')
log.debug('{table_script}: {exists}'.format(exists=os.path.exists(table_script), **locals()))

#   -i {csv,yaml,fixed,json,separator}, --input {csv,yaml,fixed,json,separator}
(rc, stdout, stderr) = run([table_script, '--help'])
# log.debug(repr(stdout))
hits = re.findall(r'--(\S+)\s+\{([^}]+)\}', stdout, flags=re.MULTILINE)
methods = {hit[0]: hit[1].split(',') for hit in hits}
log.debug('methods: {methods}'.format(**locals()))

for curr_test in [dir for dir in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, dir))]:
  print 'Testing {curr_test}'.format(**locals())
  with open(os.path.join(test_dir, curr_test, 'original.txt')) as original_stream:
    original = original_stream.read()
    run([table_script, '-i', 'fixed', '-o', 'json'], stdin=original)
