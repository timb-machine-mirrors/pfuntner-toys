#! /usr/bin/python
import platform
import subprocess
import os

class BrunoUtils:

  @staticmethod
  def cols():
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

if __name__ == "__main__":
  raise Exception("This script contains helper classes and methods and is not intended to be called directly")
