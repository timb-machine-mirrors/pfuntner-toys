#! /usr/bin/env python3

import sys

assert not sys.stdin.isatty(), 'stdin is not redirected'

byte = 0
while True:
  c = sys.stdin.read(1)
  if not c:
    break
  print('{byte:0>6} {byte:0>6x} {hex:0>2x} {c!r}'.format(hex=ord(c), **locals()))
  byte += 1
