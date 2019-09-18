#! /usr/bin/env python2

import sys
import re
import getopt

class Table:
  isNumeric = re.compile("^([-+]?(\d+\.?\d*)|(\d*\.?\d+))$")
  separators = ['|', '\t', ',', ' ']

  def __init__(self, headings, desiredSep=None, respectBlanks=False):
    assert type(headings) in (type((None,)), type([])), "Headings must be a list or tuple"

    self.respectBlanks = respectBlanks
    self.desiredSep = desiredSep
    self.headings = headings
    self.maxLens = [len(heading) for heading in self.headings]
    self.rows = []
    self.present = [False] * len(Table.separators)
    for heading in headings:
      for separator in range(len(Table.separators)):
        self.present[separator] = self.present[separator] or (Table.separators[separator] in heading)

  def add(self, row):
    assert type(row) in (type((None,)), type([])), "Row must be a list or tuple"
    assert len(row) == len(self.headings), "Expected %d columns but got %d" % (len(self.headings), len(row))

    # sys.stderr.write("Adding: %s" % (row))

    for col in range(len(row)):
      self.maxLens[col] = max(self.maxLens[col], len(row[col]))

    self.rows.append([])
    for col in row:
      data = col.strip('\n')
      if not self.respectBlanks:
        data = data.strip(' ')
      self.rows[-1].append(data)

    for col in row:
      for separator in range(len(Table.separators)):
        self.present[separator] = self.present[separator] or (Table.separators[separator] in col)

  def reverse(self):
    self.rows = self.rows[::-1]

  def sort(self, key=0):
    if type(key) == str:
      try:
        key = self.headings.index(key)
      except Exception as e:
        sys.stderr.write("Cannot sort by %s" % repr(key))
        return

    if not (0 <= key < len(self.headings)):
      sys.stderr.write("Cannot sort by %s with only %d headings" % (repr(key), len(self.headings)))
      return

    self.rows = sorted(self.rows, key=lambda datum: datum[key])

  def dump(self, stream=sys.stderr):
    stream.write(str(self.maxLens) + '\n')
    stream.write(str(self.headings) + '\n')
    for row in self.rows:
      stream.write(str(row) + '\n')

  def __str__(self):
    separator = None
    if self.desiredSep:
      separator = self.desiredSep
    else:
      for curr in range(len(self.present)):
        if not self.present[curr]:
         separator = Table.separators[curr]
         break
    assert separator, "No preferred separator found"

    ret = []
    for row in ([self.headings] + self.rows):
      line = ''
      for col in range(len(self.headings)):
        if len(line):
          line += separator
        width = self.maxLens[col]
        if not Table.isNumeric.match(row[col]):
          width = -width
        line += "%*s" % (width, row[col])
      ret.append(line.strip())
    return '\n'.join(ret)

if __name__ == "__main__":
  if sys.stdin.isatty():
    table = Table(["foobar", '*'*50])
    table.add(["This is a", "test"])
    table.add(["This", "isn't a test"])
    table.add(["Integer", "42"])
    table.add(["Float", "4.2"])
    table.add(["Float", ".2"])
    table.add(["Float", "4."])
    table.add(["Data", "2017-05-09 14:12:46,619 [myid:3] - INFO"])
    table.dump()
    print str(table)
  else:
    desiredSep = None
    (opts,args) = getopt.getopt(sys.argv[1:], "F:", ["field="])
    for (opt,arg) in opts:
      if opt in ["-F", "--field"]:
        desiredSep = arg

    line = sys.stdin.readline()
    if line:
      table = Table(line.strip('\n').split(), desiredSep=desiredSep)
      done = False
      while not done:
        line = sys.stdin.readline()
        if line:
          table.add(line.strip('\n').split())
        else:
          done = True

      print str(table)
