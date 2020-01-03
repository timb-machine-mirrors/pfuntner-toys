#! /usr/bin/env python3

import json
import sys

assert not sys.stdin.isatty(), "stdin must be redirected"

for line in sys.stdin:
  try:
    sys.stdout.write(json.dumps(json.loads(line), indent=2) + '\n')
  except Exception as e:
    sys.stdout.write(line)
