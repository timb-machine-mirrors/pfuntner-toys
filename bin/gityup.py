#! /usr/bin/env python3

import re
import sys
import json
import signal
import logging
import argparse
import datetime
import subprocess

class Git(object):
  filename_regexp = re.compile('^"(.+)"$')

  def __init__(self, log=None):
    if log:
      self.log = log
    else:
      logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
      self.log = logging.getLogger()
      mylog.setLevel(logging.WARNING)

  def repair_filename(self, filename):
    """
    Git does a little strangeness with files with special characters.  A tab always separates filenames in a line of
    output, even if the file name has an embedded tab and git will modify filenames:
      - Embedded tabs are turned into '\\t'
      - Embedded double quotes are turned into '\\"'
      - Embedded back slashes are turned into '\\\\'
      - A file name is wrapped with double quotes if it contains a tab, double quote, or back slash.
    There is no special processing for embedded spaces or single quotes.

    :param
    filename: A filename parsed from a git operation line.  It might have been massaged by git according to the above notes
    :return: The filename before git massages it:
      - Double quotes added by git to wrap the filename are removed
      - '\\t' is turned into '\t'
      - '\\"' is turned into '"'
      - '\\\\' is turned into '\\'
    """
    match = self.filename_regexp.search(filename)
    if match:
      filename = match.group(1).replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
    return filename

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

  def parse_log(self, args=[], read_from_stdin=False):
    commits = []
    # regular expression for processing `git log` output
    commit_regexp = re.compile(r'^commit\s+([0-9a-f]{40})$')  # this only retains the short SHA1: The first 7 characters
    author_regexp = re.compile(r'^Author:\s+.*<([^>]+)>$')
    date_regexp = re.compile(r'^Date:\s+((?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}\s\d{2}:\d{2}:\d{2}\s\d{4})\s([-+]\d{2})(\d{2})$')
    messages_regexp = re.compile(r'^ {4}(.*)$')
    operation_regexp = re.compile(r'^(\S+)\s+([^\t]+)(?:\s+([^\t]+))?$')

    if read_from_stdin:
      if sys.stdin.isatty():
        self.log.fatal('cannot read `git log` output from terminal')
        exit(1)
      (rc, stdout, stderr) = (0, sys.stdin.read(), '')
    else:
      (rc, stdout, stderr) = self.run(['git', 'log', '--name-status'] + args)

    if rc != 0:
      self.log.warning(f'git error: {stderr!r}')
    for line in stdout.splitlines():
      self.log.debug('Checking {line!r}, {last}'.format(line=line, last=commits[-1] if commits else None))
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
              match = operation_regexp.search(line)
              if match:
                tokens = match.groups()
                self.log.debug(f'Checking for file status in {tokens}')
                if tokens[0] == 'A':
                  commits[-1]['files'].append({'operation': 'add', 'name': self.repair_filename(tokens[1])})
                elif tokens[0] == 'M':
                  commits[-1]['files'].append({'operation': 'modify', 'name': self.repair_filename(tokens[1])})
                elif tokens[0] == 'D':
                  commits[-1]['files'].append({'operation': 'delete', 'name': self.repair_filename(tokens[1])})
                elif tokens[0] == 'Merge:':
                  commits[-1]['merge'].append(tokens[1:] if tokens[2] else tokens[1].split())
                elif tokens[0].startswith('R'):
                  commits[-1]['files'].append({
                    'operation': 'rename',
                    'old_name': self.repair_filename(tokens[1]),
                    'name': self.repair_filename(tokens[2])
                  })

    for commit in commits:
      if not (commit['merge'] or commit['files']):
        self.log.warning(f'Neither `merge` or `file` element present in {commit}')
      if not commit['merge']:
        del commit['merge']
      if not commit['files']:
        del commit['files']

    return commits

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='git log parser')
  parser.add_argument('--read-from-stdin', action='store_true', help='Get `git log` output from stdin')
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  (args, unknown_args) = parser.parse_known_args()

  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  mylog = logging.getLogger()
  mylog.setLevel(logging.WARNING - (args.verbose or 0)*10)

  signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

  gitlog = Git(mylog).parse_log(unknown_args, read_from_stdin=bool(args.read_from_stdin))
  print(json.dumps(gitlog))
