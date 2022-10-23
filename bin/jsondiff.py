#! /usr/bin/env python3

import re
import os
import json
import signal
import logging
import argparse

yaml = None

json_regexp = re.compile(r'\.json$')
yaml_regexp = re.compile(r'\.ya?ml$')

def read(filename):
  global yaml

  if os.path.exists(filename):
    if not os.path.isdir(filename):
      with open(filename) as stream:
        loader = None
        if json_regexp.search(filename):
          try:
            return json.load(stream)
          except Exception as e:
            log.fatal(f'Cannot load {filename!r}: {e!s}')
            exit(1)
        elif yaml_regexp.search(filename):
          if yaml is None:
            try:
              yaml = __import__('yaml')
            except Exception as e:
              log.fatal(f'Cannot load yaml module for {filename!r}: {e!s}')
              exit(1)
          try:
            return yaml.load(stream, Loader=yaml.BaseLoader)
          except Exception as e:
            log.fatal(f'Cannot load {filename!r}: {e!s}')
            exit(1)
        else:
          parser.error(f'Unknown type of file: {filename!r}')
    else:
      parser.error(f'Cannot process: {filename!r}')
  else:
    parser.error(f'Cannot find: {filename!r}')

class JsonDiff(object):
  def __init__(self, log=None):
    if log:
      self.log = log
    else:
      logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
      self.log = logging.getLogger()
      self.log.setLevel(logging.WARNING)

  def compare(self, root1, root2, path=[]):
    ret = True

    self.log.debug(f'Comparing {path}: {root1!r} vs {root2!r}')
    if root1 != root2:
      ret = False
      if type(root1) == type(root2):
        if isinstance(root1, list):
          if len(root1) != len(root2):
            self.log.warning('At /{path}, lhs has {size1!s} elements and rhs has {size2!s}'.format(
              path='/'.join(path),
              size1=len(root1),
              size2=len(root2),
            ))
          for pos in range(min(len(root1), len(root2))):
            ret &= self.compare(root1[pos], root2[pos], path + [str(pos)])
        elif isinstance(root1, dict):
          for key in set(root1.keys()) | set(root2.keys()):
            if key in root1 and key in root2:
              ret &= self.compare(root1[key], root2[key], path + [key])
            elif key in root1:
              self.log.warning('At /{path}, lhs has key {key}={value!r} but rhs does not'.format(
                path='/'.join(path),
                key=key,
                value=root1[key],
              ))
            else:
              self.log.warning('At /{path}, rhs has key {key}={value!r} but lhs does not'.format(
                path='/'.join(path),
                key=key,
                value=root2[key],
              ))
        else:
          self.log.warning('At /{path}, {root1!r} != {root2!r}'.format(
            path='/'.join(path),
            root1=root1,
            root2=root2,
          ))
      else:
        self.log.warning('At /{path}, lhs is {type1!s} and rhs is {type2!s}'.format(
          path='/'.join(path),
          type1=root1.__class__.__name__,
          type2=root2.__class__.__name__,
        ))

    return ret

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Compare json/yaml structures')
  parser.add_argument('file1', help='Path to file 1')
  parser.add_argument('file2', help='Path to file 2')
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  args = parser.parse_args()

  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  log.setLevel(logging.WARNING - (args.verbose or 0)*10)

  signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

  diff = JsonDiff(log=log)
  exit(0 if diff.compare(read(args.file1), read(args.file2)) else 1)
