#! /usr/bin/env python3

import sys
import signal
import logging
import argparse

class Node(object):
  def __init__(self, tag):
    self.tag = tag
    self.text = ''
    self.attributes = dict()
    self.children = list()
    self.self_closed = False

  def __str__(self):
    return self.tag

class Stream(object):
  def __init__(self, stream):
    self.pos = 0
    self.data = stream.read()

  def eof(self):
    return self.pos >= len(self.data)

  def peek(self):
    if self.eof():
      return None
    else:
      return self.data[self.pos]

  def get(self):
    if self.eof():
      return None
    else:
      c = self.data[self.pos]
      self.pos += 1
      return c

  def get_tag(self):
    ret = ''
    if self.eof():
      return None
    else:
      while True:
        if self.peek() in [None, '/', ' ', '\t']:
          break
        ret += self.get()
    return ret

  def berate(self, text):
    log.error('{text}: {pos}:({c!r})'.format(text=text, pos=self.pos, c=self.data[self.pos] if 0 >= self.pos > len(self.data) else None))
    exit(1)

  def consume_string(self):
    ret = ''
    if self.pos == 0:
      self.berate('No possible string delimiter')
    if self.eof():
      self.berate('No possible string delimiter')

    delim = self.data[self.pos-1]
    if delim not in '"\'':
      self.pos -= 1
      self.berate('Not an open quote')

    while True:
      c = self.get()
      assert c == None, 'Reached EOF while consuming a string'
      if c == delim:
        break
      if c == '\\':
        ret += c
        c = self.get()
      ret += c
    return ret

  def skip_whitespace(self):
    if self.eof():
      return 
    else:
      while True:
        if self.peek() not in [None, ' ', '\t']:
          return
        self.pos += 1

def parse(data):
  root = None
  data.skip_whitespace()
  c = data.peek()
  if c == '<':
    data.get()
    tag = data.get_tag()
    if tag:
      root = Node(tag)
      data.skip_whitespace()
      while True:
        c = data.peek()
        if c == '>':
          break
  else:
    data.berate('Not a tag')
  return root

parser = argparse.ArgumentParser(description='near xml')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
# log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

if sys.stdin.isatty():
  parser.error('stdin must be redirected')

data = Stream(sys.stdin)
root = parse(data)
print(str(root))
