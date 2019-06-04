#! /usr/bin/env python

import re
import os
import json
import logging
import argparse
import datetime
import subprocess


logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

class Boxes(object):
  def __init__(self):
    self.status_regexp = re.compile('^(\S+)\s+(\S+)\s+\(virtualbox\)$')
    self.state_regexp = re.compile('^\s+(\S+)\s+(.+)$')
    self.setup_regexp = re.compile('(\{.+\})\s*$', flags=re.DOTALL)

  @classmethod
  def run(cls, cmd, forgive=False):
    ret = None
    stdout = ''
    stderr = ''
    if isinstance(cmd, basestring):
      cmd = cmd.split()
    log.debug('Executing {cmd}'.format(**locals()))
    try:
      p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
      if forgive:
        log.info('Forgiving  `{e!s}` exception executing {cmd}'.format(**locals()))
      else:
        parser.error('Caught `{e!s}` executing {cmd}'.format(**locals()))
    else:
      (stdout, stderr) = p.communicate()
      rc = p.wait()
      log.log(logging.DEBUG if forgive or rc == 0 else logging.ERROR, '{rc}, {stdout!r}, {stderr!r}'.format(**locals()))
      if (not forgive) and (rc != 0):
        parser.error('{cmd} failed'.format(**locals()))
      return (rc, stdout, stderr)

  def boxes(self):
    ret = []
    (rc, stdout, stderr) = self.run('vagrant status', forgive=True)
    for line in stdout.splitlines():
      log.debug('Testing {line!r} against {self.status_regexp.pattern!r}'.format(**locals()))
      match = self.status_regexp.search(line)
      if match:
        box = {
          'name': match.group(1),
          'status': match.group(2),
        }
        ret.append(box)
        (rc, stdout, stderr) = self.run(['vagrant', 'ssh-config', box['name']])
        for line in stdout.splitlines():
          log.debug('Testing {line!r} against {self.state_regexp.pattern!r}'.format(**locals()))
          match = self.state_regexp.search(line)
          if match:
            box[match.group(1)] = match.group(2)

        (rc, stdout, stderr) = self.run(['ansible', box['name'], '-m', 'setup'], forgive=True)
        match = self.setup_regexp.search(stdout)
        if match:
          setup = json.loads(match.group(1))
          if setup:
            log.info('got setup')
            secs = int(setup.get('ansible_facts', {}).get('ohai_uptime_seconds', 0))
            log.info('secs: {secs}'.format(**locals()))
            if secs:
              box['uptime'] = str(datetime.timedelta(seconds=secs))

    if not ret:
      dir = '.vagrant/machines'
      if os.path.isdir(dir):
        for name in os.listdir(dir):
          ret.append({
            'name': name,
            'status': 'down',
          })
        if not ret:
          log.info('No machines in {dir} directory'.format(**locals()))
      else:
        log.info('No {dir} directory - please cd to a vagrant directory'.format(**locals()))
    return ret


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Display Vagrant systems')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  args = parser.parse_args()
  log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  print json.dumps(Boxes().boxes())
