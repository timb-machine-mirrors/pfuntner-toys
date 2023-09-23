#! /usr/bin/env python3

import os
import re
import sys
import logging
import argparse

import bruno_tools

def mkdir(*path):
  dir = os.path.join(*path)
  exists = os.path.isdir(dir)
  log.log(logging.DEBUG if exists or args.create else logging.ERROR, f'{dir} exists: {exists}')
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
        log.debug(f'{expected_string=!r} {actual_string=!r}')
        log.critical(f'{input} -> {output} mismatch')

parser = argparse.ArgumentParser(description='Test table script')
parser.add_argument('-c', '--create', dest='create', action='store_true', help='Create output')
parser.add_argument('-v', '--verbose', dest='verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

test_dir = os.path.dirname(sys.argv[0])
table_script = os.path.join(test_dir, '..', '..', 'bin', 'table.py')
log.debug(f'{table_script}: {os.path.exists(table_script)}')

#   -i {csv,yaml,fixed,json,separator}, --input {csv,yaml,fixed,json,separator}
(rc, stdout, stderr) = bruno_tools.run([table_script, '--help'], log=log)
# log.debug(repr(stdout))
hits = re.findall(r'--(\S+)\s+\{([^}]+)\}', stdout, flags=re.MULTILINE)
methods = {hit[0]: hit[1].split(',') for hit in hits}
log.debug(f'methods: {methods}')

for curr_test in [dir for dir in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, dir))]:
  print(f'Testing {curr_test}')
  with open(os.path.join(test_dir, curr_test, 'original.txt')) as original_stream:
    original = original_stream.read()
    for headings in [[], ['--headings']]:
      for input in methods['input']:
        (rc, input_string, stderr) = bruno_tools.run([table_script, '-i', 'fixed', '-o', input] + headings, stdin=original, log=log)
        mkdir(test_dir,curr_test, input)
        for output in methods['output']:
          mkdir(test_dir, curr_test, input, output)

          (rc, output_string, stderr) = bruno_tools.run([table_script, '--regexp', r'\|',  '-i', input, '-o', output] + headings, stdin=input_string, log=log)
          process(input, output, output_string, test_dir, curr_test, input, output, f'{"" if headings else "no"}headings.expected')
