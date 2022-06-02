#! /usr/bin/env python3
import re
import sys
import json
import signal
import logging
import argparse
import datetime
import subprocess

class Heading(object):
  def __init__(self, title, start, stop):
    self.title = title.strip().lower()
    self.start = start
    self.stop = stop

  def __str__(self):
    return f'{self.title}:{self.start}-{self.stop}'

# def is_mostly_numeric(s):
#   return any([bool(regexp.search(s)) for regexp in mostly_numeric_regexps])

def is_int(s):
  return bool(int_regexp.search(s))

def is_float(s):
  return bool(float_regexp.search(s))

def numify(s):
  if is_int(s):
    ret = int(s)
  elif is_float(s):
    ret = float(s)
  else:
    ret = s
  return ret


class ProcessJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if obj.__class__ in [datetime.datetime, datetime.timedelta]:
      return str(obj)
    # Let the base class default method raise the TypeError
    return obj


def evaluate(title, s):
  ret = None
  if title in ['elapsed', 'time']:
    match = timedelta_regexp.search(s)
    if match:
      ret = datetime.timedelta(
        days=int(match.group(1) or '0'),
        hours=int(match.group(2)),
        minutes=int(match.group(3)),
        seconds=int(match.group(4)),
      )
  # I wanted to do stime/start values but typical values are 'hh:mm' and 'MMMdd' which isn't very useful, IMHO
  # elif title == 'stime':
  #   try:
  #     pass
  if ret is None:
    ret = numify(s)
  return ret

def run(cmd, stdin=None, capture=True, shell=False):
  if shell:
    if isinstance(cmd, list):
      cmd = ' '.join(cmd)
  elif isinstance(cmd, str):
    cmd = cmd.split()

  log.info('Executing {cmd}'.format(**locals()))

  p = None
  try:
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE if stdin else None, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None, shell=shell)
  except Exception as e:
    (rc, stdout, stderr) = (-1, '', f'Caught {e!s} running {cmd!r}')

  if p:
    if stdin:
      p.stdin.write(stdin.encode())
    if capture:
      (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
    else:
      (stdout, stderr) = ('', '')
    rc = p.wait()

  log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

def get_gutter(start_obj, stop_obj):
  """
  Find a natural gutter between start and stop, inclusive.

  :param start_obj: The re match object of the left-hand column
  :param stop_obj: The re match object of the right-hand column
  :return: The column of the gutter (start <= return value <= stop)
  """
  log.debug(f'get_gutter({start_obj.group(0)}, {stop_obj.group(0)})')
  start = start_obj.end(0)
  stop = stop_obj.start(0)-1
  gutters = list()
  for column in range(start, stop+1):
    if all(line.rjust(column+1)[column] == ' ' for line in lines):
      gutters.append(column)

  if gutters:
    if len(gutters) == 1:
      return gutters[0]
    if gutters[-1] - gutters[0] + 1 == len(gutters):
      return gutters[0] # there's more than one potential gutter but they're all contiguous.  We'll return the first column
    else:
      log.fatal(f'Two or more potential gutters found between columns {start} ({start_obj.group(0)}) and {stop} ({stop_obj.group(0)}), inclusive: {gutters}')
      exit(1)
  else:
    log.fatal(f'No gutter found between columns {start} ({start_obj.group(0)}) and {stop} ({stop_obj.group(0)}), inclusive')
    exit(1)

SECURE_SHELL_EXECUTABLE = '/usr/bin/ssh'
PS_OPTIONS = 'user,pid,ppid,etime,time,%cpu,args'

parser = argparse.ArgumentParser(description='Get process information')

group = parser.add_mutually_exclusive_group()
group.add_argument('--ssh', help='Remote ssh host')
group.add_argument('--docker', help='Docker container ')
group.add_argument('-f', '--file', help='Path to `ps` output file to read')

parser.add_argument('--secure_shell_executable', default=SECURE_SHELL_EXECUTABLE, help=f'Path to ssh executable - default: {SECURE_SHELL_EXECUTABLE!r}')
parser.add_argument('-o', '--format', default=PS_OPTIONS, help=f'ps format (-o) - default: {PS_OPTIONS!r}'.replace('%', '%%'))
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

int_regexp = re.compile(r'^\d+$')
float_regexp = re.compile(r'^((\d+\.\d*)|(\d*\.\d+))$')

timedelta_regexp = re.compile(r'^(?:(\d+)-)?(\d{2}):(\d{2}):(\d{2})$')

# mostly_numeric_regexps = [
#   re.compile(r'^[-.0-9]([-.:0-9]*\d)?$'), # integers, floats, elapsed time, '-': some nonsensical forms are possible but I'll accept that for now.  If necessary, I can be more specific.
#   re.compile(r'^[0-9a-f]{16}$'), # signal masks - 16 digit hex string
#   re.compile(r'^(Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9 ]\d\s\d{2}:\d{2}:\d{2}\s\d{4}$'), # timestamp such as "Fri Oct 29 08:07:46 2021"
# ]

if args.file:
  with open(args.file) as stream:
    stdout = stream.read()
else:
  # /usr/bin/ssh -q aws-ubuntu2004 -- ps -e -o pid,ppid,%cpu,args
  cmd = list()
  if args.ssh:
    cmd += [args.secure_shell_executable, '-q', args.ssh]
  elif args.docker:
    cmd += ['docker', 'exec', '-it', args.docker, 'bash', '-c']

  remain = ['ps', '-e', '-o', args.format]
  if args.docker:
    cmd.append(' '.join(remain))
  else:
    cmd += remain

  (rc, stdout, stderr) = run(cmd)

if stdout and (args.file or rc == 0):
  lines = stdout.splitlines()
  gutters = list()
  heading_names = args.format.split(',')
  heading_columns = list(re.finditer('\S+', lines[0]))
  for pos in range(len(heading_columns)-1):
    gutters.append(get_gutter(heading_columns[pos], heading_columns[pos+1]))
  log.info(f'Gutters: {gutters}')

  headings = list()
  for (pos, heading) in enumerate(heading_columns):
    headings.append(Heading(heading.group(0), 0 if pos == 0 else gutters[pos-1]+1, 2**64 if pos == len(heading_columns)-1 else gutters[pos]))
  log.info(f'headings: {[str(heading) for heading in headings]}')

  processes = dict() if 'pid' in heading_names else list()
  for line in lines[1:]:
    process = {'line': line}
    for heading in headings:
      process[heading.title] = evaluate(heading.title, line[heading.start:heading.stop+1].strip())
    if isinstance(processes, dict):
      processes[process.get('pid')] = process
    else:
      processes.append(process)
  json.dump(processes, sys.stdout, indent=2, cls=ProcessJsonEncoder)
  print('')
else:
  if args.file:
    log.error(f'Nothing to read from {args.file!r}')
  else:
    log.error(f'{cmd} failed: {rc}, {stdout!r}, {stderr!r}')
  exit(1)
