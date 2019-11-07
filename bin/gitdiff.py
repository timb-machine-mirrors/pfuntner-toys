#! /usr/bin/env python2

"""
   Do `git diff` and process the output

     diff --git a/uas/workers/dep_worker.py b/uas/workers/dep_worker.py
     index 57551bb43..799cf681f 100644
     --- a/uas/workers/dep_worker.py
     +++ b/uas/workers/dep_worker.py
     @@ -49,7 +49,6 @@ from mon_utils.ssh import SSH
      from lxml import etree
      from ncclient.xml_ import *
      import re
     -from datetime import datetime
      import hashlib
      from openstack.python import client_utils
      import paramiko

"""

import re
import os
import sys
import getopt
import tempfile
import subprocess

def getoption(args, globalName, short=None, long=None, hasArgument=False):
  """
     Pull out a special option (and optional argument) from the args list without disturbing 
     options and arguments that aren't special.  For the purposes of this script, we want to
     be able to pass some command line options to `git diff` but some will be sent to the `diff`
     that we call directly.
  """

  assert (short or long) and ((not short) or (len(short) == 1))
  pos = 0
  while pos < len(args):
    arg = args[pos]
    if short and arg.startswith('-{short}'.format(**locals())):
      if hasArgument:
        globals()[globalName] = args.pop(pos+1) if (len(arg) == 2) else args[2:]
      else:
        globals()[globalName] = True
      args.pop(pos)
    elif long and arg == '--{long}'.format(**locals()):
      if hasArgument:
        globals()[globalName] = args.pop(pos+1)
      else:
        globals()[globalName] = True
      args.pop(pos)
    else:
      pos += 1
  return args # nice but not necessary: a list is an mutable object and parameter will be call-by-reference

def debug(msg):
  if verbose:
    sys.stderr.write('{msg}\n'.format(**locals()))

def complete():
  global oldfile, newfile
  if diffs:
    oldfile.flush()
    newfile.flush()

    print '\n{filename} {diffs}'.format(**globals())
    if verbose:
      subprocess.Popen(['ls', '-l', oldfile.name, newfile.name]).wait()
      subprocess.Popen(['head', oldfile.name, newfile.name]).wait()
    subprocess.Popen(['diff'] + diffOpts + [oldfile.name, newfile.name]).wait()

    oldfile.truncate(0)
    oldfile.seek(0)
    newfile.truncate(0)
    newfile.seek(0)

def show(expr):
  if verbose:
    value = eval(expr)
    print '{expr}: {value}'.format(**locals())

"""
verbose = os.environ.get('VERBOSE')
verbose = re.match('((y(e(s?)?))|(t(r(u(e?)?)?))|1)$', verbose if verbose else '', re.IGNORECASE)
"""

sideBySide = False
diffOpts = []
verbose = False
width = None

args = sys.argv[1:]
getoption(args, 'sideBySide', long='side-by-side')
getoption(args, 'verbose', short='v', long='verbose')
getoption(args, 'width', short='w', long='width', hasArgument=True)

if sideBySide:
  diffOpts.append('--side-by-side')
if width:
  diffOpts += ['--width', width]

filename_regexp = re.compile('^diff --git a/(.+) b/')
linenum_regexp = re.compile('^@@ ([^ ]+ [^ ]+) @@')
change_regexp = re.compile('^(\+|-| )(.*)$')

if sys.stdin.isatty() and (len(sys.argv) > 1):
  p = subprocess.Popen(['git', 'diff'] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = p.communicate()
  rc = p.wait()
  assert (rc == 0) and stdout and (not stderr), '`git diff` failed: {rc}, {stdout!r}, {stderr!r}'.format(**locals())
else:
  stdout = sys.stdin.read()

oldfile = tempfile.NamedTemporaryFile()
newfile = tempfile.NamedTemporaryFile()

show('oldfile.name, newfile.name')

filename = None
diffs = None
for line in stdout.splitlines():
  match = filename_regexp.search(line)
  if match:
    complete()
    filename = match.group(1)
    show('filename')
    diffs = None
  elif filename:
    match = linenum_regexp.search(line)
    if match:
      complete()
      diffs = match.group(1)
      show('diffs')
    elif diffs:
      match = change_regexp.search(line)
      if match:
        debug('{line!r} matches {pattern!r}'.format(pattern=change_regexp.pattern, **locals()))
        change_type = match.group(1)
        line = match.group(2)
        show('change_type, line')
        if change_type in ['-', ' ']:
          oldfile.write(line + '\n')
        if change_type in ['+', ' ']:
          newfile.write(line + '\n')
      else:
        debug('{line!r} does not match {pattern!r}'.format(pattern=change_regexp.pattern, **locals()))
complete()
