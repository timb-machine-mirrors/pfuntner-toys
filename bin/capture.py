#! /usr/bin/env python3

"""
  Runs a shell command, capturing stdout and stderr to a file; reporting on start time, stop time, and duration; reporting on exit status; reporting on CPU time
"""

import os
import sys
import pdb
import time
import getopt
import signal
import datetime
import threading
import subprocess
from collections import defaultdict

sigDict = defaultdict(lambda: "n/a", {getattr(signal, key): key for key in vars(signal) if key.startswith("SIG")})

def syntax(s):
  if s:
    sys.stderr.write(s + "\n")
  sys.stderr.write("Syntax: %s [-o|--output OUTPUTFILE] cmd [options ...] [arguments ...]\n" % sys.argv[0])
  exit(1)

def run(parent):
  done = False
  buffer = ""
  while not done:
    c = os.read(parent.readFd, 1)
    if c:
      parent.lock.acquire()
      buffer += c
      if c == "\n":
        parent.standardStream.write(buffer)
        parent.captureStream.write(buffer)
        buffer = ""
      parent.lock.release()
    else:
      parent.captureStream.write(buffer)
      done = True

class Capture(file):
  def __init__(self, standardStream, captureStream):
    self.standardStream = standardStream
    self.captureStream = captureStream
    self.pipe = os.pipe()
    self.readFd = self.pipe[0]
    self.writeFd = self.pipe[1]
    self.bytes = 0
    self.__closed = False
    self.lock = threading.Lock()

    self.thread = threading.Thread(target=run, args=(self,))
    self.thread.start()

    # self.closed = False
    # self.encoding = None
    # self.errors = None
    # self.mode = "w"
    # self.name = None
    # self.newlines = None
    # self.softspace = None

  @property
  def closed(self):
    return self.__closed

  @property
  def encoding(self):
    raise Exception("Not implemented")

  @property
  def errors(self):
    return None

  @property
  def mode(self):
    return "w"

  @property
  def name(self):
    raise Exception("Not implemented")

  @property
  def newlines(self):
    raise Exception("Not implemented")

  @property
  def softspace(self):
    raise Exception("Not implemented")

  def close(self):
    if not self.__closed:
      os.close(self.writeFd)
    self.__closed = True

  def flush(self):
    pass

  def fileno(self):
    return self.writeFd

  def isatty(self):
    return False

  def next(self):
    raise Exception("Not implemented")

  def read(self, size=None):
    raise Exception("Not implemented")

  def readlines(self, sizehint=None):
    raise Exception("Not implemented")

  def seek(self, offset, whence=None):
    raise Exception("Not implemented")

  def tell(self, offset, whence=None):
    return self.bytes

  def truncate(self, size=None):
    raise Exception("Not implemented")

  def write(self, s):
    os.write(self.writeFd, s)

  def writelines(self, s):
    raise Exception("Not implemented")

def signalHandler(signum, stack):
  global p
  sys.stderr.write("Caught {signame} ({signum})\n".format(signame=sigDict[signum], **locals()))

  if p:
    sys.stderr.write("Sending signal to child\n")
    p.send_signal(signum)
    # p.kill()
    time.sleep(1)

  print("Goodbye, cruel world")
  os._exit(1)

(opts,args) = ([],[])
try:
  (opts,args) = getopt.getopt(sys.argv[1:], "do:", ["debug", "output="])
except Exception as e:
  syntax(str(e))

captureFilename = None
captureDir = "."
p = None
debug = False

for (opt,arg) in opts:
  if opt in ["-o", "--output"]:
    if os.path.isdir(arg):
      captureDir = arg
    else:
      captureFilename = arg
  elif opt in ["-d", "--debug"]:
    debug = not debug
  else:
    syntax("Don't know how to handle %s" % repr(opt))

if debug:
  pdb.set_trace()

if not args:
  syntax("No arguments present")

if not captureFilename:
  captureFilename = os.path.join(captureDir, "{base}-{now:%Y%m%d%H%M%S%f}.out".format(base=os.path.basename(sys.argv[0]), now=datetime.datetime.now()))

captureFile = open(captureFilename, "w", 0)
print("Writing to %s" % repr(captureFilename))

stdoutCapture = Capture(sys.stdout, captureFile)
stderrCapture = Capture(sys.stderr, captureFile)

stdoutCapture.write("Running: {cmd}\n".format(cmd=str(args)))

signal.signal(signal.SIGINT, signalHandler)

start = datetime.datetime.now()
p = subprocess.Popen(args, stdout=stdoutCapture, stderr=stderrCapture)
(pid, status, stats) = os.wait3(0)
stop = datetime.datetime.now()

stdoutCapture.write("\nStart: {start}\nStop: {stop}\nDuration: {duration}\n".format(start=start.isoformat(), stop=stop.isoformat(), duration=stop-start))
stdoutCapture.write("Status: {status:04x}, rc={rc}".format(status=status, rc=status/256))
signum = status%256
if signum:
  stdoutCapture.write(", signal={signame} ({signum})".format(signame=sigDict[signum], **locals()))
stdoutCapture.write("\n")
stdoutCapture.write("User: {user:.2f}s, System: {system:.2f}s\n".format(user=stats.ru_utime, system=stats.ru_stime))

stdoutCapture.close()
stderrCapture.close()

print("Wrote to %s" % repr(captureFilename))

exit(status/256)
