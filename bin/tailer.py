#! /usr/bin/env python2

# this is similar to the tail command but it reads from the very beginning of the stdin and keeps reading

import os
import sys

assert not sys.stdin.isatty(), "stdin must be directed"
assert len(sys.argv) == 1, "No parameters are expected"

sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', 0)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

while True:
  line = sys.stdin.readline()
  sys.stdout.write(line)
