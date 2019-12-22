#! /usr/bin/env python3

import os
import re
import sys
import json
import base64
import os.path
import hashlib
import getpass
import logging
import argparse
import datetime

def syntax(msg=None):
  if msg:
    sys.stderr.write(msg + "\n")
  parser.print_help(sys.stderr)
  exit(1)

def berate(s):
  global output

  if args.jsonOutput:
    if not ("errors" in output):
      output["errors"] = [s]
    else:
      output["errors"].append(s)
  else:
    log.info("%s" % s)

def announce(name, value, whisperName=False):
  if args.jsonOutput:
    output["pairs"][name] = value
  else:
    if whisperName:
      print(value)
    else:
      print("%s: %s" % (name, value))

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
  def __init__(self, filename, key=None, keyPromptForMissingFile=True, ssh=False):
    global log

    self.simpleFilename = filename
    self.store = {}
    self.exists = False
    self.fernet = None

    if '/' in filename:
      if filename[0] == '/':
        self.filename = filename
      else:
        self.filename = os.path.join(os.getcwd(), filename)
    else:
      self.filename = os.path.join("%s/.private" % getHome(), filename)

    log.debug('store is {self.filename}'.format(**locals()))

    if ssh and (not key):
      sshFilename = '%s/.ssh/id_rsa' % getHome()
      if os.path.isfile(sshFilename):
        log.debug('Reading {sshFilename}'.format(**locals()))
        with open(sshFilename) as stream:
          key = ''.join([line for line in stream.read().splitlines() if not re.match('---', str(line))])
          log.debug('ssh private key is {bytes} bytes long'.format(bytes=len(key)))

    if keyPromptForMissingFile or os.path.exists(self.filename):
      done = False

      while not done:
        if key:
          self.simpleKey = key
        else:
          self.simpleKey = getpass.getpass("Key for %s: " % repr(self.simpleFilename))
  
        hash = hashlib.md5()
        hash.update(self.simpleKey.encode('utf-8'))
        self.key = base64.b64encode(hash.hexdigest())

        try:
          fernet = __import__('cryptography.fernet', fromlist=['Fernet'])
          self.fernet = fernet.Fernet(self.key)
        except Exception as e:
          log.info('Caught `{e!s}` trying to load cryptography.fernet'.format(**locals()))
          return
  
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
    global log

    if os.path.isfile(self.filename):
      backup =  self.filename + "D" + datetime.datetime.now().isoformat().replace(':', '')
      log.info('Backing up {self.filename} to {backup}'.format(**locals()))
      os.rename(self.filename, backup)
    else:
      dir = os.path.dirname(self.filename)
      if not os.path.isdir(dir):
        os.mkdir(dir, 0o700)
    log.info('Saving store to {self.filename}'.format(**locals()))
    with open(self.filename, 'w') as f: 
      f.write(self.fernet.encrypt(json.dumps(self.store)))

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

if __name__ == "__main__":
  output = {"pairs": {}}

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

  parser = argparse.ArgumentParser(description='A manager of secure stores')
  parser.add_argument('-o', '--operation', dest='operation', help='Secure store operation', choices=['read', 'get', 'set', 'remove', 'test'], required=True)
  parser.add_argument('-s', '--store', dest='storeName', help='Name of secure store')

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-k', '--key', dest='key', help='Encryption key for secure store')
  group.add_argument('--ssh', dest='ssh', action='store_true', help='Use ssh private key for secure store encryption key')

  parser.add_argument('-j', '--json', dest='jsonOutput', action='store_true', help='Print output in JSON form')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging messages')
  parser.add_argument('args', metavar='arg', nargs='*', help='Additional arguments, dependent on operation')
  args = parser.parse_args()

  log.setLevel(logging.DEBUG if args.verbose else logging.ERROR)

  if args.operation != "test" and (not args.storeName):
    syntax('Use -s/--store to specify secure store')

  if args.operation == "test":
    store = SecureKeyValues("test", "this is a test")
    print("store file: %s" % store.filename)
    keys = store.keys()
    print("keys: %s" % keys)
    if keys:
      for key in keys:
        print("%s: %s" % (key, store.get(key)))
      store.put("runs", [str(datetime.datetime.now())] + store.get("runs"))
    else:
      store.put("one", 1)
      store.put("two", 2)
      store.put("one hundred", 100)
      store.put("runs", [])
    store.write()
  else:
    store = SecureKeyValues(args.storeName, args.key, keyPromptForMissingFile=(args.operation != "read"), ssh=args.ssh)
    keyvalue_regexp = re.compile("^([^=]+)=(.+)$")
    key_regexp = re.compile("^(\w[^=]*\w+)$")
    if args.operation == "read":
      if not store.exists:
        berate("%s does not exist" % repr(store.filename))
      for key in store.keys():
        announce(key, store.get(key))
    elif args.operation == "set":
      if not args.args and sys.stdin.isatty():
        args.args = sys.stdin.read().strip('\n').split('\n')
      for arg in args.args:
        match = keyvalue_regexp.search(str(arg))
        if match:
          store.put(match.group(1), match.group(2))
        else:
          match = key_regexp.search(str(arg))
          if match:
            store.put(match.group(1), getpass.getpass('Enter value for {name!r}: '.format(name=match.group(1))))
          else:
            parser.error('{arg!r} is neither a valid key nor key/value pair'.format(**locals()))
      store.write()
    elif args.operation == "remove":
      for arg in args.args:
        store.remove(arg)
      store.write()
    elif args.operation == "get":
      for arg in args.args:
        match = staticStringRegexp.search(str(arg))
        if match:
          if (not args.jsonOutput):
            print(match.group(1))
        else:
          announce(arg, store.get(arg), whisperName=True)

  if args.jsonOutput:
    print(json.dumps(output, indent=2, sort_keys=True))
