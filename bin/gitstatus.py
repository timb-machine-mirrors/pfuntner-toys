#! /usr/bin/env python2

import re
import sys
import getopt
import subprocess

"""
ibmadmin@pfuntner1:~/tmp/pseudo-logmet-login$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Untracked files:
  (use "git add <file>..." to include in what will be committed)

        Dockerfile
        cert.pem
        docker-compose.yml
        pseudologin.json
        pseudologin.py
"""

def syntax(msg=None):
  if msg:
    sys.stderr.write("%s\n" % msg)
  sys.stderr.write("Syntax: %s --all|%s [--noparents]\n" % (sys.argv[0], '|'.join(["--%s" % section for section in sections])))
  exit(1)

sections = ["untracked", "changes"]

noParents = False

desired = {}
inSection = {}
for section in sections:
  desired[section] = False
  inSection[section] = False

(opts,args) = getopt.getopt(sys.argv[1:], "", sections + ["all", "noparents", "noparent"])
for (opt,arg) in opts:
  short = opt[2:]
  if short in sections:
    desired[short] = not desired[short]
  elif opt == "--all":
    for section in sections:
      desired[section] = True
  elif opt in ["--noparents", "--noparent"]:
    noParents = not noParents
  else:
    syntax("Unhandled option `%s`" % opt)

if sum([desired[section] for section in sections]) == 0:
  syntax()

p = subprocess.Popen(["git", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout,stderr) = p.communicate()
assert p.wait() == 0, "`git status` rc=%d, %s, %s" % (p.returncode, stdout, stderr)

for line in stdout.split('\n'):
  if re.match("\S", line):
    for section in sections:
      inSection[section] = re.match(section.title(), line) != None
  elif re.match("\s+[^ \t(]", line) and ((not noParents) or ("../" not in line)):
    for section in sections:
      if inSection[section] and desired[section]:
        if inSection["changes"]:
          match = re.search("modified:\s+(\S*)", line)
          if match:
            print match.group(1).strip(' \r')
        else:
          print line.strip(' \r')
