#! /usr/bin/env python

import sys
import logging
import argparse
import subprocess

class Table(object):
  def __init__(self, *args):
    if len(args) == 1 and type(args[0]) in (list, tuple):
      self.headings = args[0]
    else:
      self.headings = args

    try:
      self.p = subprocess.Popen(['column', '-t', '-s\t'], stdin=subprocess.PIPE, text=True)
    except Exception as e:
      print(f'Error opening `column`: {e!s}', file=sys.stderr)
      print('On Ubuntu, try installing the bsdmainutils package', file=sys.stderr)
      exit(1)

    self.p.stdin.write('\t'.join([str(heading) for heading in self.headings]) + '\n')

  @classmethod
  def encode(cls, s):
    return s if sys.version_info.major == 2 else s.encode()

  def add(self, *args):
    self.p.stdin.write('\t'.join([str(arg) for arg in args]) + '\n')

  def close(self):
    self.p.stdin.close()
    self.p.wait()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Test simpletable')
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  args = parser.parse_args()
  
  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  log.setLevel(logging.WARNING - (args.verbose or 0)*10)

  table = Table('col1', 'col2')
  table.add('r1c1', 'r1c2')
  table.add('row 2, column 1', 'row 2, column 2')
  table.close()
