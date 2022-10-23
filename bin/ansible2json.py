#! /usr/bin/env python3

"""
   Turn Ansible output into full JSON.  It's pretty close to JSON but
   not quite.  Here's an example of using it:

     $ docker exec ansible ansible localhost -m ping | ansible2json
        [WARNING]: provided hosts list is empty, only localhost is available
     [
       {
         "changed": false,
         "host": "localhost",
         "ping": "pong",
         "result": "SUCCESS"
       }
     ]
     $

   In this example, a container called `ansible` is expected to be running - that's why `ansible` appears "twice" on the command line.

   The script adds the `host` and `result` elements - they come from Ansible but are not part of the JSON structure that Ansible prints with the other elements (`ping` and `changed`).
"""

import re
import sys
import json

assert not sys.stdin.isatty(), 'stdin must be redirected'

verbose = False

def debug(msg):
  if verbose:
    sys.stderr.write('{msg}\n'.format(**locals()))

regexp = re.compile('^(\S+)\s\|\s(\S+)\s=>\s\{$')

buf = ''
host = None
result = None

results = []
while True:
  line = sys.stdin.readline()
  if not line:
    break
  if buf:
    buf += line
    try:
      results.append(json.loads(buf))
    except Exception as e:
      pass
    else:
      results[-1]['host'] = host
      results[-1]['result'] = result
      host = None
      result = None
      buf = ''
  else:
    line = line.strip('\n').strip('\r')
    match = regexp.search(str(line))
    debug('{line!r}: {match}'.format(**locals()))
    if match:
      host = match.group(1)
      result = match.group(2)
      buf = '{'

assert not buf, 'Unclosed result buffer: {buf!r}'.format(**locals())

print(json.dumps(results, indent=2, sort_keys=True))
