#! /usr/bin/env python3

import re
import os
import logging
import datetime
import platform
import subprocess

"""
  A trick for bootstrapping this module when it's not in the same directory
  as the calling script:

    #! /usr/bin/python
    
    import os
    import sys
    import exceptions
    
    try:
      import BrunoUtils
    except exceptions.ImportError as e:
      retry = False
    
      if "PYTHONPATH" not in os.environ:
        retry = True
      else:
        retry = ("$(HOME)s/bin" % os.environ) not in os.environ["PYTHONPATH"].split(':')
    
      if retry:
        sys.stderr.write("Retrying with PYTHONPATH=%(HOME)s/bin to find BrunoUtils...\n" % os.environ)
        os.environ["PYTHONPATH"] = "%(HOME)s/bin" % os.environ
        os.execvp("python", ["python"] + sys.argv)
      else:
        sys.stderr.write("`%s` even after retry!  Are you sure the module is in $(HOME)s/bin?\n" % (str(e), os.environ))
        exit(1)
"""

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
# log.setLevel(logging.DEBUG)

class BrunoUtils:

  @classmethod
  def extract(cls, cmd, pattern, default_value):
    ret = default_value
    caster = type(ret)
    if isinstance(cmd, list):
      cmd = ' '.join(cmd)
    log.debug('Running {cmd!r}'.format(**locals()))
    try:
      p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      (stdout, stderr) = p.communicate()
      stdout = stdout.decode('utf-8')
      stderr = stderr.decode('utf-8')
      rc = p.wait()
      log.debug('{cmd!r}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
      match = re.search(pattern, stdout)
      if match:
        log.debug('extracted: {}'.format(match.group(1)))
        ret = caster(match.group(1))
      else:
        log.debug('{stdout!r} failed to match {pattern!r}'.format(**locals()))
    except Exception as e:
      log.debug('Caught `{e!s}`'.format(**locals()))

    return ret

  @classmethod
  def cols(cls):
    """
      This is designed to return the number of columns in the user's display.

      Return value: The number of columns as an integer.
    """

    return cls.extract('stty size < /dev/tty', '\d+\s+(\d+)', 80)

  @classmethod
  def rows(cls):
    """
      This is designed to return the number of rows in the user's display.

      Return value: The number of rows as an integer.
    """

    return cls.extract('stty size < /dev/tty', '(\d+)\s+\d+', 24)

  @staticmethod
  def divmod(a, b):
    x = int(a/b)
    return (x, a-(x*b))
  
  @staticmethod
  def see(o, secondsOnly=False):
    """
      This is designed to format a timedelta object or the number of seconds between
      two dates (a floating point number) in a nice standard way, optionally breaking 
      it down into hours, minutes, etc.

      Arguments:
        - o: A timedelta object or a floating point number
        - secondsOnly: An optional boolean argument that tells the method whether or
          not to break seconds into hours, minutes, etc or just leave them as seconds 

      Returns:
        A string like:
          "01.05s"
          "02h00m00.00s"
    """
    ret = ""
  
    if type(o) in [float, datetime.timedelta]:
  
      if type(o) == float:
        secs = o
      else:
        secs = o.total_seconds()
  
      if secondsOnly:
        days = 0
        hours = 0
        mins = 0
      else:
        (days, secs) = BrunoUtils.divmod(secs, 24*60*60)
        (hours, secs) = BrunoUtils.divmod(secs, 60*60)
        (mins, secs) = BrunoUtils.divmod(secs, 60)
  
      if days > 0:
        ret += "%dd" % days
      if ret or (hours > 0):
        ret += "%02dh" % hours
      if ret or (mins > 0):
        ret += "%02dm" % mins
      ret += "%05.2fs" % secs
    else:
      raise Exception("Don't know how to handle a %s" % str(type(o)))
  
    return ret

  @classmethod
  def get_file(cls, filename):
    if os.path.exists(filename):
      assert not os.path.isdir(filename), f'{filename} is a directory'
      size = os.path.getsize(filename)
      if size > 2**20:
        altname = filename + '-' + datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f')
        subprocess.Popen(['mv', filename, altname]).wait()
        subprocess.Popen(['gzip', altname]).wait()
    return filename

class TimezoneMagic(object):
  """
  As the name implies, this class has some methods to perform some timezone magic.  I needed a way to compare the
  current date with an arbitrary date: both dates are expressed in local time but either  could be in daylight savings
  time which can mess up comparisons by an hour or so.

  Additionally, since there have been different rules about when daylight savings time begins and ends over the years,
  I've tried to account for the most recent rules in the United States from about the mid-1960's.

  The most useful methods:
    - to_gmt(): convert a datetime object expressed in local time to gmt
    - is_in_dst(): Determines if a datetime object is in daylight savings time or not
  """
  def __init__(self):
    now = datetime.datetime.now()
    self.utc = datetime.datetime.utcnow()

    diff = now - self.utc if now > self.utc else self.utc - now

    in_dst = self.is_in_dst(now)
    if in_dst:
      self.dst_offset = round(diff.total_seconds())
      self.std_offset = self.dst_offset + 60 * 60
    else:
      self.std_offset = round(diff.total_seconds())
      self.dst_offset = self.std_offset - 60 * 60

  def locate_sunday(self, month, year, occurrence):
    """
    Get n-th Sunday of week for a month/year
    :param month: Month as an integer: 1=January, ..., 12=December
    :param year: Year (including century) as an integer such as 2020
    :param occurrence: Which occurence of the weekday: 1: first, 2: second, ... -1: last (could be 4th or 5th)
    :return: A datetime object representing the desired date
    """

    log.info(f'Seeking {occurrence}-th Sunday of {month}/{year}')

    if occurrence >= 1:
      curr = datetime.datetime.strptime(f'{year}/{month}/01 02:00:00', '%Y/%m/%d %H:%M:%S')
      step = datetime.timedelta(days=1)
      while occurrence > 0:
        log.info(f'Examining {curr!s}')
        if curr.weekday() == 6:
          if occurrence == 1:
            break
          else:
            occurrence -= 1
        curr += step
    elif occurrence == -1:
      # begin at start of next month so we don't have to worry if this month has 28, 29, 30, or 31 days!
      month += 1
      curr = datetime.datetime.strptime(f'{year}/{month}/01 02:00:00', '%Y/%m/%d %H:%M:%S')
      step = datetime.timedelta(days=1)
      curr -= step # this places us on the last day of the desired month
      while curr.weekday() != 6:
        curr -= step
    else:
      log.error(f'Occurrence of `{occurrence}` is not supported!')

    log.info(f'Desired Sunday is {curr!s}')
    return curr

  def is_in_dst(self, curr):
    """

      From https://www.wikiwand.com/en/Standard_time_in_the_United_States

      2007-present: 2nd Sunday March, 1st Sunday November
      1987-2006:    1st Sunday April, last Sunday October
      1975:       	Sun February 23 - October 26 (Emergency Daylight Time Act)
      1974:       	Sun January 6 - October 27 (Emergency Daylight Time Act)
      1966-1986:    last Sunday April, last Sunday October

    """
    dst_start = None
    dst_end = None
    if curr.year >= 2007:
      dst_start = self.locate_sunday(3, curr.year, 2)
      dst_end = self.locate_sunday(11, curr.year, 1)
    elif 1987 <= curr.year <= 2006:
      dst_start = self.locate_sunday(4, curr.year, 1)
      dst_end = self.locate_sunday(10, curr.year, -1)
    elif curr.year == 1975:
      log.debug('Be aware that 1975 had the weird-ass `Emergency Daylight Time Act`')
      dst_start = datetime.datetime.strptime('1975/02/23 02:00:00', '%Y/%m/%d %H:%M:%S')
      dst_end = datetime.datetime.strptime('1975/10/26 02:00:00', '%Y/%m/%d %H:%M:%S')
    elif curr.year == 1974:
      log.debug('Be aware that 1974 had the weird-ass `Emergency Daylight Time Act`')
      dst_start = datetime.datetime.strptime('1974/01/06 02:00:00', '%Y/%m/%d %H:%M:%S')
      dst_end = datetime.datetime.strptime('1974/10/27 02:00:00', '%Y/%m/%d %H:%M:%S')
    elif 1966 <= curr.year <= 1986:
      dst_start = self.locate_sunday(4, curr.year, -1)
      dst_end = self.locate_sunday(10, curr.year, -1)
    else:
      log.error(f'Do not know when DST starts/ends in {curr.year}')
      exit(1)
    log.info(f'In {curr.year}, DST began at {dst_start!s} and ended at {dst_end!s}')

    in_dst = dst_start <= curr < dst_end
    log.info('{curr!s} is in {zone}'.format(curr=curr, zone='daylight savings time' if in_dst else 'standard time'))
    return in_dst

  def to_gmt(self, curr):
    in_dst = self.is_in_dst(curr)

    if curr < self.utc:
      curr += datetime.timedelta(seconds=self.dst_offset if in_dst else self.std_offset)
    else:
      curr -= datetime.timedelta(seconds=self.dst_offset if in_dst else self.std_offset)

    return curr

if __name__ == "__main__":
  raise Exception("This script contains helper classes and methods and is not intended to be called directly")
