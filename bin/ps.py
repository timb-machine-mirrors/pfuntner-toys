#! /usr/bin/env python3

"""
  The information is extracted from files under /proc.  See `man proc`.
"""

import os
import re
import sys
import glob
import json
import time
import signal
import logging
import datetime
import argparse
import subprocess

class Ps(object):
  kv_regexp = re.compile('^(\S+):\s*(.*)$')

  def __init__(self, log=None):
    if log is None:
      logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
      self.log = logging.getLogger()
      self.log.setLevel(logging.WARNING)
    else:
      self.log = log

  def read(self, path, mode=''):
    ret = None
    try:
      with open(path, 'r' + mode) as stream:
        ret = stream.read()
        if 'b' in mode:
          ret = ret.decode()
    except Exception as e:
      log.debug(f'Could not read {path!r}: {e!s}')
  
    log.debug(f'{path!r}: {ret!r}')
  
    return ret
  
  def int_or_none(self, s):
    ret = s
    if s is not None:
      ret = int(s)
    return ret
  
  def kv_parse(self, s):
    ret = dict()
    if s is not None:
      for line in s.splitlines():
        match = self.kv_regexp.search(line)
        if match:
          ret[match.group(1)] = match.group(2).strip()
      
    return ret
  
  def get_processes(self):
    processes = {}
    
    now_seconds = time.time()
    now = datetime.datetime.fromtimestamp(now_seconds)
    
    up_time_seconds = float(self.read('/proc/uptime').split()[0])
    boot_time_seconds = now_seconds - up_time_seconds
    
    seconds_per_jiffy = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    
    for path in glob.glob(os.path.join('/proc', '[0-9]*')):
      pid = int(os.path.basename(path))
    
      cmdline = self.read(os.path.join(path, 'cmdline'), 'b')
      if cmdline is not None:
        cmdline = cmdline.strip('\0').split('\0')
        if cmdline == ['']:
          cmdline = []
        cmdline = ' '.join(cmdline)
    
      stat = self.read(os.path.join(path, 'stat'))
      stat_tokens = stat.split() if stat else [None] * 52
    
      statm = self.read(os.path.join(path, 'statm'))
      statm_tokens = statm.split() if stat else [None] * 7
    
      status_dict = self.kv_parse(self.read(os.path.join(path, 'status')))
      log.info(f'status_dict: {status_dict}')
    
      processes[pid] = {
        'pid': pid,
        'ppid': self.int_or_none(stat_tokens[3]),
    
        'cmdline': cmdline,
    
        'state': stat_tokens[2],
        'pgrp': self.int_or_none(stat_tokens[4]),
        'session': self.int_or_none(stat_tokens[5]),
        'tty_nr': self.int_or_none(stat_tokens[6]),
        'tpgid': self.int_or_none(stat_tokens[7]),
        'flags': '0x{:08x}'.format(int(stat_tokens[8])),
        'minflt': self.int_or_none(stat_tokens[9]),
        'cminflt': self.int_or_none(stat_tokens[10]),
        'majflt': self.int_or_none(stat_tokens[11]),
        'cmajflt': self.int_or_none(stat_tokens[12]),
        'utime': self.int_or_none(stat_tokens[13]),
        'stime': self.int_or_none(stat_tokens[14]),
        'cutime': self.int_or_none(stat_tokens[15]),
        'cstime': self.int_or_none(stat_tokens[16]),
        'priority': self.int_or_none(stat_tokens[17]),
        'nice': self.int_or_none(stat_tokens[18]),
        'num_threads': self.int_or_none(stat_tokens[19]),
        'itrealvalue': self.int_or_none(stat_tokens[20]),
    
        'starttime': self.int_or_none(stat_tokens[21]),
    
        'vsize': self.int_or_none(stat_tokens[22]),
        # 'rss': self.int_or_none(stat_tokens[23]), # inaccurate -> see /proc/PID/statm
        'rsslim': self.int_or_none(stat_tokens[24]),
        'startcode': self.int_or_none(stat_tokens[25]),
        'endcode': self.int_or_none(stat_tokens[26]),
        'startstack': self.int_or_none(stat_tokens[27]),
        'kstkesp': self.int_or_none(stat_tokens[28]),
        'kstkeip': self.int_or_none(stat_tokens[29]),
        # 'signal': self.int_or_none(stat_tokens[30]), # obsolete -> see /proc/PID/status
        # 'blocked': self.int_or_none(stat_tokens[31]), # obsolete -> see /proc/PID/status
        # 'sigignore': self.int_or_none(stat_tokens[32]), # obsolete -> see /proc/PID/status
        # 'sigcatch': self.int_or_none(stat_tokens[33]), # obsolete -> see /proc/PID/status
        'wchan': self.int_or_none(stat_tokens[34]), # obsolete -> see /proc/PID/status
        # 'nswap': self.int_or_none(stat_tokens[35]), # not maintained
        # 'cnswap': self.int_or_none(stat_tokens[36]), # not maintained
        'exit_signal': self.int_or_none(stat_tokens[37]),
        'processor': self.int_or_none(stat_tokens[38]),
        'rt_priority': self.int_or_none(stat_tokens[39]),
        'policy': self.int_or_none(stat_tokens[40]),
        'delayacct_blkio_ticks': self.int_or_none(stat_tokens[41]),
        'guest_time': self.int_or_none(stat_tokens[42]),
        'cguest_time': self.int_or_none(stat_tokens[43]),
        'start_data': self.int_or_none(stat_tokens[44]),
        'end_data': self.int_or_none(stat_tokens[45]),
        'start_brk': self.int_or_none(stat_tokens[46]),
        'arg_start': self.int_or_none(stat_tokens[47]),
        'arg_end': self.int_or_none(stat_tokens[48]),
        'env_start': self.int_or_none(stat_tokens[49]),
        'env_end': self.int_or_none(stat_tokens[50]),
        'exit_code': self.int_or_none(stat_tokens[51]),
    
        'size': self.int_or_none(statm_tokens[0]),
        'resident': self.int_or_none(statm_tokens[1]),
        'shared': self.int_or_none(statm_tokens[2]),
        'text': self.int_or_none(statm_tokens[3]),
        # 'lib': self.int_or_none(statm_tokens[4]), # unused, always 0
        'data': self.int_or_none(statm_tokens[5]),
        'dt': self.int_or_none(statm_tokens[6]), # unused, always 0
    
        'umask': status_dict.get('Umask'),
        'vmpeak': status_dict.get('VmPeak'),
        'vmsize': status_dict.get('VmSize'),
        'vmlck': status_dict.get('VmLck'),
        'vmpin': status_dict.get('VmPin'),
        'vmhwm': status_dict.get('VmHWM'),
        'vmrss': status_dict.get('VmRSS'),
        'rssanon': status_dict.get('RssAnon'),
        'rssfile': status_dict.get('RssFile'),
        'rssshmem': status_dict.get('RssShmem'),
        'vmdata': status_dict.get('VmData'),
        'vmstk': status_dict.get('VmStk'),
        'vmexe': status_dict.get('VmExe'),
        'vmlib': status_dict.get('VmLib'),
        'vmpte': status_dict.get('VmPTE'),
        'vmpmd': status_dict.get('VmPMD'),
        'sigq': status_dict.get('SigQ'),
        'sigpnd': status_dict.get('SigPnd'),
        'shdpnd': status_dict.get('ShdPnd'),
        'sigblk': status_dict.get('SigBlk'),
        'sigign': status_dict.get('SigIgn'),
        'sigcgt': status_dict.get('SigCgt'),
        'capinh': status_dict.get('CapInh'),
        'capprm': status_dict.get('CapPrm'),
        'capeff': status_dict.get('CapEff'),
        'capbnd': status_dict.get('CapBnd'),
        'nonewprivs': status_dict.get('NoNewPrivs'),
        'seccomp': status_dict.get('Seccomp'),
        'speculation_store_bypass': status_dict.get('Speculation_Store_Bypass'),
        'cpus_allowed': status_dict.get('Cpus_allowed'),
        'cpus_allowed_list': status_dict.get('Cpus_allowed_list'),
        'mems_allowed': status_dict.get('Mems_allowed').split(','),
        'mems_allowed_list': status_dict.get('Mems_allowed_list'),
        'voluntary_ctxt_switches': status_dict.get('voluntary_ctxt_switches'),
        'nonvoluntary_ctxt_switches': status_dict.get('nonvoluntary_ctxt_switches'),
      }
    
      processes[pid]['starttime_seconds'] = boot_time_seconds + processes[pid]['starttime'] / seconds_per_jiffy
    
      starttime = datetime.datetime.fromtimestamp(processes[pid]['starttime_seconds'])
      processes[pid]['starttime_iso'] = starttime.isoformat()
      elapsed = now - starttime
      processes[pid]['elapsed_seconds'] = elapsed.total_seconds()
      processes[pid]['elapsed_timedelta'] = str(elapsed)

    return processes

if __name__ ==  '__main__':
  parser = argparse.ArgumentParser(description='Generate process information in JSON')
  
  # group = parser.add_mutually_exclusive_group()
  # group.add_argument('-s', '--ssh', help='Remote ssh host to query')
  # group.add_argument('-d', '--docker', help='Docker container query')
  
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  args = parser.parse_args()
  
  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  log.setLevel(logging.WARNING - (args.verbose or 0)*10)
  
  signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))
  
  json.dump(Ps(log).get_processes(), sys.stdout, indent=2)
