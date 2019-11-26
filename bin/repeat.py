#! /usr/bin/env python2

import sys
import time
import getopt
import subprocess

def syntax(msg=None):
  if msg:
    sys.stderr.write('{msg}\n'.format(**locals()))
  sys.stderr.write('Syntax: {pgm} -c|--count COUNT [-i|--interval SECONDS] CMD ...\n'.format(pgm=sys.argv[0]))
  exit(1)

(opts,args) = ([], [])
try:
  (opts,args) = getopt.getopt(sys.argv[1:], 'c:i:', ['count=', 'interval='])
except Exception as e:
  syntax(str(e))

count = None
interval = 0
for (opt,arg) in opts:
  if opt in ['-c', '--count']:
    count = int(arg)
    if count <= 0:
      syntax('count must be greater than 0')
  elif opt in ['-i', '--interval']:
    interval = float(arg)
    if interval <= 0:
      syntax('interval must be greater than 0')
  else:
    syntax('Unexpected option: {opt!r}'.format(**locals()))

if not count:
  syntax('Specify a count')

if not args:
  syntax('A command is required')

for iteration in range(count):
  p=subprocess.Popen(args)
  p.wait()
  if iteration < (count-1):
    time.sleep(interval)
