#! /usr/bin/env python3

import sys

assert not sys.stdin.isatty(), "stdin must be redirected"
assert len(sys.argv) == 3, "Syntax: %s old-string new-string, received %s" % (sys.argv[0], sys.argv)

sys.stdout.write(sys.stdin.read().replace(eval("'%s'" % sys.argv[1]), eval("'%s'" % sys.argv[2])))
