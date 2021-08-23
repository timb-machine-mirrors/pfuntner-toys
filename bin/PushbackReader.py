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
    """
      I've seen instances of multibyte sequences in the place of double quotes.  On 2021-08-14,
      http://cnn.com/index.html contained:

        .
        .
        .
        <link rel="dns-prefetch" href="//fastlane-adv.rubiconproject.com" /> ...
        <link rel="dns-prefetch" href=”//ib.adnxs.com”/> ...
        <link rel="dns-prefetch" href=”//prebid.adnxs.com”/>
        .
        .
        .

      I used my hexes tool to look more carefully at the data and saw:

        00001085 000001 00001085 0x68 104 0150 'h'
        00001086 000001 00001086 0x72 114 0162 'r'
        00001087 000001 00001087 0x65 101 0145 'e'
        00001088 000001 00001088 0x66 102 0146 'f'
        00001089 000001 00001089 0x3d  61 0075 '='
        00001090 000001 00001090 0xe2 226 0342 'â'
        00001091 000001 00001091 0x80 128 0200 '\x80'
        00001092 000001 00001092 0x9d 157 0235 '\x9d'
        00001093 000001 00001093 0x2f  47 0057 '/'
        00001094 000001 00001094 0x2f  47 0057 '/'
        00001095 000001 00001095 0x69 105 0151 'i'
        00001096 000001 00001096 0x62  98 0142 'b'
        00001097 000001 00001097 0x2e  46 0056 '.'
        00001098 000001 00001098 0x61  97 0141 'a'
        00001099 000001 00001099 0x64 100 0144 'd'
        00001100 000001 00001100 0x6e 110 0156 'n'
        00001101 000001 00001101 0x78 120 0170 'x'
        00001102 000001 00001102 0x73 115 0163 's'
        00001103 000001 00001103 0x2e  46 0056 '.'
        00001104 000001 00001104 0x63  99 0143 'c'
        00001105 000001 00001105 0x6f 111 0157 'o'
        00001106 000001 00001106 0x6d 109 0155 'm'
        00001107 000001 00001107 0xe2 226 0342 'â'
        00001108 000001 00001108 0x80 128 0200 '\x80'
        00001109 000001 00001109 0x9d 157 0235 '\x9d'

      I will turn those sequences into double quotes.
    """
    self.buf = self.buf.replace(chr(8221), '"')

    self.pos = 0

    # self.newlines keeps track of where the newlines are in the file which is used by the location() method
    self.newlines = [curr for curr in range(len(self.buf)) if self.buf[curr] == '\n']
    log.debug(f'newlines: {self.newlines}')

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
    location = self.location()
    while True:
      c = self.read()
      if c not in self.whitespace:
        break
    self.log.debug(f'Read {c!r} at {location}')
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
      if self.pos <= self.newlines[linenum]:
        break
      linenum += 1

    linenum = min(linenum + 1, len(self.newlines))
    if linenum == 1:
      column = self.pos + 1
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
  # os.fdopen(w, 'w').write('  This is a\n  test\n')
  #
  # reader = PushbackReader(r, log=log)
  #
  # print(f'pos: {reader.pos}')
  # print(f'location: {reader.location()}')
  # content = reader.read(64)
  # print(f'content: {content!r}')
  # print(f'pos: {reader.pos}')
  # print(f'location: {reader.location()}')
  #
  # reader.push(content)
  # content = reader.read(64)
  # print(f'content: {content!r}')
  # print(f'pos: {reader.pos}')
  #
  # reader.push(content)
  # c = reader.skip_spaces()
  # print(f'c: {c!r}')
  # print(f'pos: {reader.pos}')
  # print(f'location: {reader.location()}')
  #
  # c = reader.read()
  # print(f'c: {c!r}')
  # print(f'pos: {reader.pos}')
  # print(f'location: {reader.location()}')
  #
  # print('This will thrown an exception because the expected string will not match the actual string')
  # reader.push(content)

  os.fdopen(w, 'w').write('''<html>
  <p>This is a test
</html>
''')

  reader = PushbackReader(r, log=log)
  while True:
    location = reader.location()
    c = reader.read()
    if not c:
      break
    print(f'{c!r} {location}')
