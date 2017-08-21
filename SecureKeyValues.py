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

class SecureKeyValues:
  def __init__(self, filename, key=None):
    self.simpleFilename = filename
    self.store = {}

    if key:
      self.simpleKey = key
    else:
      self.simpleKey = getpass.getpass("Key: ")

    hash = hashlib.md5()
    hash.update(self.simpleKey)
    self.key = base64.b64encode(hash.hexdigest())
    self.fernet = Fernet(self.key)

    if '/' in filename:
      if filename[0] == '/':
        self.filename = filename
      else:
        self.filename = os.path.join(os.getcwd(), filename)
    else:
      self.filename = os.path.join("%(HOME)s/.private" % os.environ, filename)

    if os.path.isfile(self.filename):
      with open(self.filename, 'r') as f: 
        self.store = json.loads(self.fernet.decrypt(f.read()))

  def get(self, key):
    if key in self.store:
      return self.store[key]
    else:
      return None

  def put(self, key, value):
    self.store[key] = value

  def keys(self):
    return self.store.keys()

  def remove(self, key):
    if key in self.store:
      return self.store.pop(key)
    else:
      return None

  def write(self):
    if os.path.isfile(self.filename):
      os.rename(self.filename, self.filename + "D" + datetime.datetime.now().isoformat())
    with open(self.filename, 'w') as f: 
      f.write(self.fernet.encrypt(json.dumps(self.store)))

if __name__ == "__main__":
  operation = None
  key = None
  storeName = None

  (opts,args) = getopt.getopt(sys.argv[1:], "k:o:s:", ["key=", "operation=", "store="])
  for (opt,arg) in opts:
    if opt in ["-o", "--operation"]:
      operation = arg
    elif opt in ["-k", "--key"]:
      key = arg
    elif opt in ["-s", "--store"]:
      storeName = arg

  assert (operation == "test") or (storeName and (operation in ["read", "set", "remove"])), "Syntax: %s --store STORE --key KEY --operation test|read|set|remove <args>" % sys.argv[0]

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
    store = SecureKeyValues(storeName, key)
    if operation == "read":
      for key in store.keys():
          print "%s: %s" % (key, store.get(key))
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
    else:
      sys.stderr.write("Don't know how to handle operation %s\n" % repr(operation))
