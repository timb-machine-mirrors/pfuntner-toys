#! /usr/bin/env python3

import os
import io
import sys
import string
import logging
import argparse

class PushbackReader(object):
  def __init__(self, src, log=None):
    """
    The constructor takes various sources and builds a simple reader class that allows you push
    bytes back into the buffer as if they have not been read.
    :param src: The source of the data.  It can be:
      - An integer representing a file descriptor
      - A string representing a file name
      - A file object which is ready to go
    :param log: The optional logging object of the caller.
    """
    if log:
      self.log = log
    else:
      logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
      self.log = logging.getLogger('PushbackReader')
      self.log.setLevel(logging.WARNING)

    self.whitespace = [c for c in string.whitespace]

    # figure out the type of source and build a stream from it if necessary
    self.src = src
    self.log.debug(f'src is a {src.__class__.__name__}')
    if isinstance(src, io.IOBase):
      if src == sys.stdin and sys.stdin.isatty():
        log.fatal('stdin must be redirected')
        exit(1)
      self.stream = src
    elif isinstance(src, int):
      self.stream = os.fdopen(src, 'r')
    elif isinstance(src, str):
      self.stream = open(src, 'r')
    else:
      raise(Exception(f'Unexpected source: {src.__class__.__name__}'))

    self.buf = self.stream.read()
    self.pos = 0

    # self.newlines keeps track of where the newlines are in the file which is used by the location() method
    self.newlines = [curr for curr in range(len(self.buf)) if self.buf[curr] == '\n']

  def read(self, bytes=1):
    """
    Read the next 0 or more bytes from the stream
    :param bytes: A integer for the number of bytes to read
    :return: A string presenting the data read.  Its length will be no more than `bytes` characters but it could be
    less.  The method returns None if it is at EOF
    """
    ret = self.buf[self.pos:self.pos+bytes]
    self.pos = min(self.pos+bytes, len(self.buf))
    if ret == '':
      ret = None
    return ret

  def skip_spaces(self):
    """
    Return the next character that is not whitespace
    :return: A single character for the next non-whitespace character.  The method returns None if it is at EOF
    """
    c = None
    while True:
      c = self.read()
      if c not in self.whitespace:
        break
    return c

  def push(self, expected):
    """
    Push a string with a length of 0 or more.
    :param expected: The string to push back onto the stream.  Given a string of N characters, the last N characters
    of the stream at the current position must EXACTLY MATCH the expected string or else an exception is thrown.  After
    successfully pushing the string, read(N) would return the exact same string.

    If `expected is None`, the method acts like `expected == ''`
    :return: None
    """
    if expected is None:
      expected = ''
    actual = self.buf[max(self.pos-len(expected), 0):self.pos]
    if actual != expected:
      raise Exception(f'Data mismatch: Expected {expected!r} but actual is {actual!r}')
    self.pos -= len(expected)

  def location(self):
    """
    Report the current logical location in the stream.  The initial location is line 1, column 1
    :return: A string in the form '{line number}:{column number}'
    """
    linenum = 0
    while linenum < len(self.newlines):
      self.log.debug(f'{self.pos} < {self.newlines[linenum]} ?')
      if self.pos < self.newlines[linenum]:
        break
      linenum += 1

    linenum = min(linenum + 1, len(self.newlines))
    if linenum == 1:
      column = 1 if self.pos == 0 else self.pos
    else:
      column = self.pos - self.newlines[linenum-2]
    return f'{linenum}:{column}'

  def peek(self, expected):
    """
    Determine if the upcoming bytes match an expected string
    :param expected: The string to test the stream against
    :return: True if the next characters in the stream match the expected string, False otherwise
    """
    return self.buf[self.pos:self.pos+len(expected)] == expected

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Test PushbackReader class')
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  args = parser.parse_args()
  
  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  log.setLevel(logging.WARNING - (args.verbose or 0)*10)

  (r, w) = os.pipe()
  os.fdopen(w, 'w').write('  This is a\n  test\n')

  reader = PushbackReader(r, log=log)

  print(f'pos: {reader.pos}')
  print(f'location: {reader.location()}')
  content = reader.read(64)
  print(f'content: {content!r}')
  print(f'pos: {reader.pos}')
  print(f'location: {reader.location()}')

  reader.push(content)
  content = reader.read(64)
  print(f'content: {content!r}')
  print(f'pos: {reader.pos}')

  reader.push(content)
  c = reader.skip_spaces()
  print(f'c: {c!r}')
  print(f'pos: {reader.pos}')
  print(f'location: {reader.location()}')

  c = reader.read()
  print(f'c: {c!r}')
  print(f'pos: {reader.pos}')
  print(f'location: {reader.location()}')

  print('This will thrown an exception because the expected string will not match the actual string')
  reader.push(content)
