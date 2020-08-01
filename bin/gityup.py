#! /usr/bin/env python3

import re
import json
import signal
import logging
import argparse
import datetime
import subprocess

class Git(object):
  def __init__(self, log=None):
    if log:
      self.log = log
    else:
      logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
      self.log = logging.getLogger()
      mylog.setLevel(logging.WARNING)

  def run(self, cmd, capture=True):
    if isinstance(cmd, str):
      cmd = cmd.split()
    self.log.info('Executing {cmd}'.format(**locals()))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    if capture:
      (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
    else:
      (stdout, stderr) = ('', '')
    rc = p.wait()
    self.log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
    return (rc, stdout, stderr)

  def git_timestamp_parse(self, groups):
    main = groups[0]
    hours_offset = int(groups[1])
    minutes_offset = int(groups[2])

    date = datetime.datetime.strptime(main, '%a %b %d %H:%M:%S %Y')
    if hours_offset >= 0:
      date -= datetime.timedelta(hours=hours_offset, minutes=minutes_offset)
    else:
      date += datetime.timedelta(hours=-hours_offset, minutes=minutes_offset)
    return str(date) # .isoformat().replace('-', '.').replace(':', '').replace('T', '-')

  def parse_log(self, args=[]):
    commits = []
    # regular expression for processing `git log` output
    commit_regexp = re.compile(r'^commit\s+([0-9a-f]{40})$')  # this only retains the short SHA1: The first 7 characters
    author_regexp = re.compile(r'^Author:\s+.*<([^>]+)>$')
    date_regexp = re.compile(r'^Date:\s+((?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}\s\d{2}:\d{2}:\d{2}\s\d{4})\s([-+]\d{2})(\d{2})$')
    messages_regexp = re.compile(r'^ {4}(.*)$')
    file_status_regexp = re.compile('^[A-Za-z]')

    (rc, stdout, stderr) = self.run(['git', 'log', '--name-status'] + args)
    for line in stdout.splitlines():
      self.log.debug(f'Checking {line!r}')
      match = commit_regexp.search(line)
      if match:
        commits.append({'messages': [], 'files': [], 'merge': []})
        commits[-1]['commit'] = match.group(1)
      else:
        match = author_regexp.search(line)
        if match:
          commits[-1]['author'] = match.group(1)
        else:
          match = date_regexp.search(line)
          if match:
            commits[-1]['utc_date'] = self.git_timestamp_parse(match.groups())
          elif commits:
            match = messages_regexp.search(line)
            if match:
              commits[-1]['messages'].append(match.group(1))
            else:
              match = file_status_regexp.search(line)
              if match:
                tokens = line.split()
                self.log.debug(f'Checking for file status in {tokens}')
                if tokens[0] == 'A':
                  commits[-1]['files'].append({'operation': 'add', 'name': tokens[1]})
                elif tokens[0] == 'M':
                  commits[-1]['files'].append({'operation': 'modify', 'name': tokens[1]})
                elif tokens[0] == 'D':
                  commits[-1]['files'].append({'operation': 'delete', 'name': tokens[1]})
                elif tokens[0] == 'Merge:':
                  commits[-1]['merge'].append(tokens[1:])
                elif tokens[0].startswith('R'):
                  commits[-1]['files'].append({'operation': 'rename', 'old_name': tokens[1], 'name': tokens[2]})

    for commit in commits:
      assert bool(commit['merge']) ^ bool(commit['files']), f'Either `merge` or `file` element expected in {commit}'
      if not commit['merge']:
        del commit['merge']
      if not commit['files']:
        del commit['files']

    return commits

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='git log parser')
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  (args, unknown_args) = parser.parse_known_args()

  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  mylog = logging.getLogger()
  mylog.setLevel(logging.WARNING - (args.verbose or 0)*10)

  signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

  gitlog = Git(mylog).parse_log(unknown_args)
  print(json.dumps(gitlog))
