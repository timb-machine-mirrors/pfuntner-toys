#! /usr/bin/python

import os
import re
import sys
import json
import base64
import getopt
import os.path
import hashlib
import getpass
import datetime
from cryptography.fernet import Fernet

def syntax(msg=None):
  if msg:
    sys.stderr.write(msg + "\n")
  sys.stderr.write("Syntax: %s --store STORE --key KEY --operation test|read|set|remove <args>\n" % sys.argv[0])
  exit(1)

def berate(s):
  if jsonOutput:
    if not ("errors" in output):
      output["errors"] = [s]
    else:
      output["errors"].append(s)
  else:
    sys.stderr.write("%s\n" % s)

def announce(name, value, whisperName=False):
  if jsonOutput:
    output["pairs"][name] = value
  else:
    if whisperName:
      print value
    else:
      print "%s: %s" % (name, value)

def tryHome(name):
  ret = None
  if (name in os.environ) and os.path.isdir(os.environ[name]):
    ret = os.environ[name]
  return ret

def getHome():
  ret = None

  ret = tryHome("HOME")
  if not ret:
    ret = tryHome("USERPROFILE")

  assert ret, "Cannot determine your home directory"
  return ret

class SecureKeyValues:
  def __init__(self, filename, key=None, keyPromptForMissingFile=True):
    self.simpleFilename = filename
    self.store = {}
    self.exists = False

    if '/' in filename:
      if filename[0] == '/':
        self.filename = filename
      else:
        self.filename = os.path.join(os.getcwd(), filename)
    else:
      self.filename = os.path.join("%s/.private" % getHome(), filename)

    if keyPromptForMissingFile or os.path.exists(self.filename):
      done = False
      while not done:
        if key:
          self.simpleKey = key
        else:
          self.simpleKey = getpass.getpass("Key for %s: " % repr(self.simpleFilename))
  
        hash = hashlib.md5()
        hash.update(self.simpleKey)
        self.key = base64.b64encode(hash.hexdigest())
        self.fernet = Fernet(self.key)
  
        if os.path.isfile(self.filename):
          with open(self.filename, 'r') as f: 
            try:
              self.store = json.loads(self.fernet.decrypt(f.read()))
              self.exists = True
              done = True
            except Exception as e:
              sys.stderr.write("Exception: %s ... try again\n" % repr(e))
              key = None
        else:
          """
            The lack of a store file is not a problem.  It will get created once
            the write() method is used on the object.  We have a key and will
            use it if and when we write.
          """
          done = True

  def get(self, key, root=None):
    if root == None:
      root = self.store

    if type(key) != list:
      key = key.split("/")

    if key[0] in root:
      return root[key[0]] if len(key) == 1 else self.get(key[1:], root[key[0]])
    else:
      return None

  def put(self, key, value, root=None):
    if root == None:
      root = self.store

    if type(key) != list:
      key = key.split("/")

    if len(key) > 1:
      if key[0] not in root:
        root[key[0]] = {}
        self.put(key[1:], value, root[key[0]])
    else:
      root[key[0]] = value

  def keys(self):
    return self.store.keys()

  def remove(self, key):
    if key in self.store:
      return self.store.pop(key)
    else:
      return None

  def write(self):
    if os.path.isfile(self.filename):
      os.rename(self.filename, self.filename + "D" + datetime.datetime.now().isoformat().replace(':', ''))
    dir = os.path.dirname(self.filename)
    if not os.path.isdir(dir):
      os.mkdir(dir, 0700)
    with open(self.filename, 'w') as f: 
      f.write(self.fernet.encrypt(json.dumps(self.store)))

if __name__ == "__main__":
  output = {"pairs": {}}

  operation = None
  key = None
  storeName = None
  jsonOutput = False

  """
    `staticStringRegexp` is a regular expression that let's us
    identify when an argument is a "static string".  That is,
    the caller wants the string included in the result as-is
    and the store is not used.  This can be used to build
    calls like this:

      $ echo $(SecureKeyValues --store foobar --get \"-u\" user \"-p\" password)
      Key for 'ctc':
      -u fooar -p bar
      $
  """
  staticStringRegexp = re.compile("^['\"](.+)['\"]$")

  (opts,args) = ([], [])
  try:
    (opts,args) = getopt.getopt(sys.argv[1:], "h?k:o:s:j", ["help", "key=", "operation=", "store=", "json"])
  except Exception as e:
    syntax(str(e))

  for (opt,arg) in opts:
    if opt in ["-o", "--operation"]:
      operation = arg
    elif opt in ["-k", "--key"]:
      key = arg
    elif opt in ["-s", "--store"]:
      storeName = arg
    elif opt in ["-j", "--json"]:
      jsonOutput = not jsonOutput
    elif opt in ["-?", "--help"]:
      syntax()
    else:
      raise Exception("Don't know how to handle option %s" % repr(opt))

  if not((operation == "test") or (storeName and (operation in ["read", "get", "set", "remove"]))):
    syntax()

  if operation == "test":
    store = SecureKeyValues("test", "this is a test")
    print "store file: %s" % store.filename
    keys = store.keys()
    print "keys: %s" % keys
    if keys:
      for key in keys:
        print "%s: %s" % (key, store.get(key))
      store.put("runs", [str(datetime.datetime.now())] + store.get("runs"))
    else:
      store.put("one", 1)
      store.put("two", 2)
      store.put("one hundred", 100)
      store.put("runs", [])
    store.write()
  else:
    store = SecureKeyValues(storeName, key, keyPromptForMissingFile=(operation != "read"))
    if operation == "read":
      if not store.exists:
        berate("Note: %s does not exist" % repr(store.filename))
      for key in store.keys():
        announce(key, store.get(key))
    elif operation == "set":
      regexp = re.compile("^([^=]+)=(.*)$")
      if not args and sys.stdin.isatty():
        args = sys.stdin.read().strip('\n').split('\n')
      for arg in args:
        match = regexp.search(arg)
        assert match and (len(match.groups()) == 2), "%s did not match %s" % (repr(arg), repr(regexp.pattern))
        store.put(match.group(1), match.group(2))
      store.write()
    elif operation == "remove":
      for arg in args:
        store.remove(arg)
      store.write()
    elif operation == "get":
      for arg in args:
        match = staticStringRegexp.search(arg)
        if match:
          if (not jsonOutput):
            print match.group(1)
        else:
          announce(arg, store.get(arg), whisperName=True)
    else:
      berate("Don't know how to handle operation %s\n" % repr(operation))

  if jsonOutput:
    print json.dumps(output, indent=2, sort_keys=True)
