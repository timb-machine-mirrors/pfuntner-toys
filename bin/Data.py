#! /usr/bin/env python

import sys
import random
import string
import datetime
import uuid
import json

class Data:
  NUMBER_RANGE = 2**32
  MIN_NAME_LENGTH = 4
  MAX_NAME_LENGTH = 16
  MAX_YEAR = 2500
  MIN_JSON_ITEMS = 4
  MAX_JSON_ITEMS = 10

  def __init__(self):
    self.values = [method for method in dir(Data) if method.startswith("get") and method not in ["getListOfDicts", "getValue"]]

  @staticmethod
  def getNumber():
    return random.uniform(-Data.NUMBER_RANGE/2, Data.NUMBER_RANGE/2-1)

  @staticmethod
  def getInteger():
    return random.randint(-Data.NUMBER_RANGE/2, Data.NUMBER_RANGE/2-1)

  @staticmethod
  def getName():
    return ''.join([random.choice(string.lowercase) for iter in
                    range(random.randint(Data.MIN_NAME_LENGTH, Data.MAX_NAME_LENGTH))])

  @staticmethod
  def getDatetime():
    return datetime.datetime(1, 1, 1) + datetime.timedelta(seconds=random.randint(0, Data.MAX_YEAR*365*24*60*60*1000)/1000.0)

  @staticmethod
  def getUuid():
    return str(uuid.uuid4())

  @staticmethod
  def getBoolean():
    return random.choice([False, True])

  def getValue(self, pos=None):
    value = Data.getName()
    return value

  def getListOfDicts(self):
    items = []
    keys = [Data.getName() for iter in range(random.randint(Data.MIN_JSON_ITEMS, Data.MAX_JSON_ITEMS))]
    for itemNum in range(random.randint(Data.MIN_JSON_ITEMS, Data.MAX_JSON_ITEMS)):
      item = {}
      for (pos, key) in list(enumerate(keys)):
        item[key] = str(getattr(self, self.values[pos%len(self.values)])())

      items.append(item)
    return items

if __name__ == "__main__":
  iterations = range(10)

  data = Data()

  if len(sys.argv) == 1:
    print json.dumps({
      "numbers": [data.getNumber() for iter in iterations],
      "integers": [data.getInteger() for iter in iterations],
      "names": [data.getName() for iter in iterations],
      "dates": [data.getDatetime().isoformat() for iter in iterations],
      "uids": [data.getUuid() for iter in iterations],
      "booleans":  [data.getBoolean() for iter in iterations],
      "listOfDicts": data.getListOfDicts(),
    })
  elif len(sys.argv) == 2:
    if sys.argv[1] == "getListOfDicts":
      print json.dumps(data.getListOfDicts())
    else:
      try:
        pos = data.values.index(sys.argv[1])
      except:
        sys.stderr.write("{arg!r} is not one of the valid methods: {valid}, getListOfDicts\n".format(
          arg=sys.argv[1],
          valid=', '.join(data.values)
        ))
        exit(1)
      else:
        print json.dumps(getattr(data, data.values[pos])())
