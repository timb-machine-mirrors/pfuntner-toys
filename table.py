#! /usr/bin/python

import sys
import re

class Table:
  isNumeric = re.compile("^([-+]?(\d+\.?\d*)|(\d*\.?\d+))$")
  separators = ['|', '\t', ',', ' ']

  def __init__(self, headings):
    assert type(headings) in (type((None,)), type([])), "Headings must be a list or tuple"
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
      self.rows[-1].append(col.strip('\n').strip(' '))

    for col in row:
      for separator in range(len(Table.separators)):
        self.present[separator] = self.present[separator] or (Table.separators[separator] in col)

  def dump(self, stream=sys.stderr):
    stream.write(str(self.maxLens) + '\n')
    stream.write(str(self.headings) + '\n')
    for row in self.rows:
      stream.write(str(row) + '\n')

  def __str__(self):
    separator = None
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
      ret.append(line)
    return '\n'.join(ret)

if __name__ == "__main__":
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
