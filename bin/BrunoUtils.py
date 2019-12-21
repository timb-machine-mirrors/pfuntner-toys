#! /usr/bin/env python3
import platform
import subprocess
import os
import datetime

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

class BrunoUtils:

  @staticmethod
  def cols():
    """
      This is designed to return the number of columns in the user's display.

      Return value: The number of columns as an integer.
    """

    tput_cols=None
    try:
      if platform.python_version() >= "2.7":
        tput_output = subprocess.check_output(["tput", "cols"])
      else:
        tput_file = os.popen("tput cols")
        tput_output = tput_file.read()
        tput_file.close()
      tput_cols = int(tput_output)
    except Exception as e:
      pass
    return tput_cols

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

if __name__ == "__main__":
  raise Exception("This script contains helper classes and methods and is not intended to be called directly")
