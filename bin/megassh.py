#! /usr/bin/env python3

import os
import sys
import json
import getopt
import os.path
import logging
import argparse
import datetime
import subprocess

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

isSSH = False
isSCP = False

if "ssh" in sys.argv[0]:
  isSSH = True
elif "scp" in sys.argv[0]:
  isSCP = True
else:
  log.critical('Command is not ssh or scp')
  exit(1)

parser = argparse.ArgumentParser(description='Perform ssh commands across remote machines' if isSSH else 'Copy files across remote machines')
parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Display only output from machines')

group = parser.add_mutually_exclusive_group()
group.add_argument('--only', dest='only', help='Comma-separated list of machines on which to ' + ('execute' if isSSH else 'copy'))
group.add_argument('--not', dest='nots', help='Comma-separated list of machines on which to NOT ' + ('execute' if isSSH else 'copy'))

if isSSH:
  parser.add_argument('-j', '--json', action='store_true', help='Print results in JSON form')
  parser.add_argument('cmd', help='Command to execute')
  parser.add_argument('args', metavar='arg', nargs='*', help='Arguments for command to execute')
else:
  parser.add_argument('-r', '--recursive', dest='recursive', help='Copy files recursively')
  parser.add_argument('src', nargs='+', help='One or more local source files from which to copy')
  parser.add_argument('dest', help='Remote machine destination')

parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
args = parser.parse_args()

log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

onlyList = args.only.split(',') if args.only else []
notList = args.nots.split(',') if args.nots else []

systems = None

pgm = sys.argv[0]
if pgm[-3:] == ".py":
  pgm = pgm[:-3]

jsonFile = pgm + ".json"
if args.verbose:
  log.debug("opening %s" % jsonFile)

with open(jsonFile, 'r') as f:
  systems = json.load(f)

log.info("Hosts: %s" % systems)

for system in systems:

  if ((not onlyList) and (not notList)) or (onlyList and (system["name"] in onlyList)) or (notList and (system["name"] not in notList)):
    if isSSH:
      if (not args.quiet) and (not args.json):
        print("%s" % (system["name"]))
      cmd = [args.cmd] + args.args
  
    else:
      # for src in args[:-1]:
      #   if not quiet:
      #     print "%s @ %s" % (src, system["name"])
      #
      #     cmd = [src, "%s@%s:%s" % (system["user"], system["host"], args[-1])]

      push = None
      cmd = []
      name = system["name"]
      host = system["host"]
      user = system["user"]
      remote = "{user}@{host}".format(**locals())

      for filename in args.src:
        src = filename.format(remote=remote)
        pushing = not src.startswith(remote + ":")
        if (push != None) and (pushing != push):
          sys.stderr.write("Cannot change scp direction with %s" % repr(filename))
          exit(1)
        push = pushing
        cmd.append(src)

      dst = args.dest.format(remote=remote, host=host, user=user)
      if (dst == args[-1]) and pushing:
        dst = "{remote}:{dst}".format(**locals())
      cmd.append(dst)

      print("%s: %s" % (name, ' '.join(cmd)))
  
    if isSSH:
      cmd = ["%s@%s" % (system["user"], system["host"])] + cmd
  
    if "key" in system:
      cmd = ["-i", system["key"]] + cmd
  
    cmd = ["-o", "LogLevel=quiet"] + cmd
  
    if isSCP and args.recursive:
      cmd.insert(0, "-r") # -r should only be able to be specified if we're "megascp"

    cmd = ["ssh" if isSSH else "scp"] + cmd
  
    log.debug(cmd)
  
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    rc = p.wait()
    log.debug("rc=%d, `%s`, `%s`\n" % (rc, repr(stdout.strip('\n')), repr(stderr.strip(''))))
    if isSSH and args.json:
      print(json.dumps({)
        'rc': rc,
        'stdout': stdout.splitlines(),
        'stderr': stderr.splitlines(),
        'host': system['host'],
        'time': str(datetime.datetime.utcnow()),
      }, sort_keys=True)
    else:
      sys.stdout.write(stdout)
      sys.stderr.write(stderr)
