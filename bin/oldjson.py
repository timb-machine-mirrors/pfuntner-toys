#! /usr/bin/env python

import sys
import getopt
import json
import itertools

def syntax(msg):
    if msg:
        sys.stderr.write(msg + "\n")
    sys.stderr.write("Syntax: %s [--yaml] [--fromstr] [--verbose] [--flatten] [--describe] [--file FILENAME] [--depth DEPTH] [--forgive] [--linear] [--string] [--empty] [path ...]\n" % sys.argv[0])
    exit(1)

def shorten(s, maxLen=80):
    if len(s) > maxLen:
        s = s[:maxLen/2-1] + "..." + s[-(maxLen/2-2):]
    return s

def flatWriter(root, path=[]):
    if type(root) == list:
      if root:
        for curr in range(len(root)):
          flatWriter(root[curr], path + [str(curr)])
      elif empty:
        print '/%s/' % '/'.join(path)
    elif type(root) == dict:
      if root:
        for curr in sorted(root.keys()):
          flatWriter(root[curr], path + [str(curr)])
      elif empty:
        print '/%s/' % '/'.join(path)
    else:
      if type(root) == unicode:
        root = str(root)
      print "/%s %s" % ("/".join(path), repr(root))

def jsonWriter(root):
    print json.dumps(root, indent=2, sort_keys=True)

def stringWriter(root):
  print json.dumps(root, sort_keys=True)

def linearWriter(root):
    if isinstance(root, list):
      for datum in root:
        print json.dumps(datum, sort_keys=True)
    elif isinstance(root, dict):
      for key in sorted(root.keys()):
        print json.dumps({key: root[key]}, sort_keys=True)
    else:
      print json.dumps(root, sort_keys=True)

def stripNulls(items):
    items = list(items)
    if forgive:
        items = [item for item in items if item != None]
    return items

def process(root, path):
    ret = root
    if path:
        curr = path[0]
        if type(root) == list:
            if curr == "*":
                ret = stripNulls(itertools.imap(process, iter(root), itertools.repeat(path[1:])))
            else:
                try:
                    curr = int(curr)
                except Exception as e:
                    sys.stderr.write("Could not cast %s to a list index\n" % repr(curr))
                else:
                    if curr >= len(root):
                        sys.stderr.write("Addressing index %d but there are only %d items\n" % (repr(curr), len(root)))
                        if forgive:
                            ret = None
                        else:
                            exit(1)
                    else:
                        ret = process(root[curr], path[1:])
        elif type(root) == dict:
            if curr == "*":
                ret = stripNulls(itertools.imap(process, iter(root.values()), itertools.repeat(path[1:])))
            elif curr in root:
                ret = process(root[curr], path[1:])
            else:
                sys.stderr.write("Addressing non-existent index %s\n" % repr(curr))
                if forgive:
                    ret = None
                else:
                    exit(1)
        else:
            sys.stderr.write("At %s, expected a list of dictionary but got a %s\n" % (repr(curr), type(root)))
            exit(1)
    return ret

def describeWriter(root):
    if type(root) == list:
        print "A %d element list" % len(root)
    elif type(root) == dict:
        print "A %d element dictionary with keys: %s" % (len(root.keys()), ', '.join(sorted(root.keys())))
    else:
        print "A %s" % type(root)

def lop(root, depth):
    if depth <= 0:
        if type(root) == list:
            for (key, value) in enumerate(root):
                root[key] = shorten(json.dumps(value, sort_keys=True))
        elif type(root) == dict:
            for (key, value) in [(key, root[key]) for key in root.keys()]:
                root[key] = shorten(json.dumps(value, sort_keys=True))
    else:
        if type(root) == list:
            itertools.imap(lop, root, itertools.repeat(depth-1))
        elif type(root) == dict:
            for key in root.keys():
                lop(root[key], depth-1)

verbose = False
fromstr = False
describe = False
writer = jsonWriter
filename = None
depth = None
forgive = False
inputIsYaml = False
empty = False

(opts, args) = ([], [])
try:
    (opts,args) = getopt.getopt(sys.argv[1:], "v", ["verbose", "fromstr", "flat", "flatten", "describe", "file=", "depth=", "forgive", 'linear', 'string', 'yaml', 'empty'])
except Exception as e:
    syntax(str(e))

for (opt,arg) in opts:
    if opt in ["-v", "--verbose"]:
        verbose = not verbose
    elif opt in ["--flat", "--flatten"]:
        writer = flatWriter
    elif opt == "--fromstr":
        fromstr = not fromstr
    elif opt == "--describe":
        writer = describeWriter
    elif opt == "--linear":
        writer = linearWriter
    elif opt == "--string":
        writer = stringWriter
    elif opt == "--file":
        filename = arg
    elif opt == "--depth":
        try:
            depth = int(arg)
        except Exception as e:
            syntax("Could not parse `%s %s`: %s" % (opt, arg, e))
    elif opt == "--forgive":
       forgive = not forgive
    elif opt == "--yaml":
       inputIsYaml = not inputIsYaml
       import yaml
    elif opt == "--empty":
       empty = not empty
    else:
        syntax("Don't know how to handle %s" % repr(opt))

data = None

if filename:
    with open(filename) as stream:
        data = stream.read()
else:
    if sys.stdin.isatty():
        syntax("stdin must be redirected if not file name is specified")
    data = sys.stdin.read()

if fromstr:
  data = json.dumps(eval(data))

root = None
try:
    if inputIsYaml:
      root = yaml.load(data)
    else:
      root = json.loads(data)
except Exception as e:
    syntax("Could not parse %s: %s" % (repr(shorten(data)), str(e)))

if len(args) == 1:
    args = args[0].strip('/').split('/')

root = process(root, args)

if depth != None:
  lop(root, depth)

writer(root)
