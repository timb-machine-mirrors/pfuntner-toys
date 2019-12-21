#! /usr/bin/env python2

import os
import re
import sys
import logging
import argparse
import subprocess

def run(cmd, stdin=None, forgive=False):
  if isinstance(cmd, str):
    cmd = cmd.split()
  p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = p.communicate(stdin or '')
  rc = p.wait()
  fail = (rc != 0) or stderr
  log.log(logging.ERROR if fail else logging.DEBUG,
          '{cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  if fail:
    exit(1)
  return (rc, stdout, stderr)

def mkdir(*path):
  dir = os.path.join(*path)
  exists = os.path.isdir(dir)
  log.log(logging.DEBUG if exists or args.create else logging.ERROR,
          '{dir} exists: {state}'.format(state=exists, **locals()))
  if not exists:
    if args.create:
      os.mkdir(dir)
    else:
      exit(1)

def process(input, output, actual_string, *path):
  with open(os.path.join(*path), 'w' if args.create else 'r') as stream:
    if args.create:
      stream.write(actual_string)
    else:
      expected_string = stream.read()
      if actual_string != expected_string:
        log.critical('{input} -> {output} mismatch'.format(**locals()))
        exit(1)

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
(rc, stdout, stderr) = run([table_script, '--help'], forgive=True)
# log.debug(repr(stdout))
hits = re.findall(r'--(\S+)\s+\{([^}]+)\}', stdout, flags=re.MULTILINE)
methods = {hit[0]: hit[1].split(',') for hit in hits}
log.debug('methods: {methods}'.format(**locals()))

for curr_test in [dir for dir in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, dir))]:
  print 'Testing {curr_test}'.format(**locals())
  with open(os.path.join(test_dir, curr_test, 'original.txt')) as original_stream:
    original = original_stream.read()
    for headings in [[], ['--headings']]:
      for input in methods['input']:
        (rc, input_string, stderr) = run([table_script, '-i', 'fixed', '-o', input] + headings, stdin=original)
        mkdir(test_dir,curr_test, input)
        for output in methods['output']:
          mkdir(test_dir, curr_test, input, output)

          (rc, output_string, stderr) = run([table_script, '--regexp', r'\|',  '-i', input, '-o', output] + headings,
                                            stdin=input_string)
          process(input, output, output_string, test_dir, curr_test, input, output,
                  '{state}headings.expected'.format(state='' if headings else 'no'))
