#! /usr/bin/env python

class Decolorizer:
  escape = '\033'

  def __init__(self):
    self.items = 0

  def process(self, item):
    item = str(item)
    if self.items == 0 and item.startswith(self.escape + '[0m' + self.escape):
      item = item[4:]
    if item.startswith((self.escape + '[01;', self.escape + '[40;')) and item.endswith(self.escape + '[0m\n'):
      first = item.find('m')
      if first > 5:
        item = item[first+1:]
        item = item[:-5] + '\n'
    elif item == self.escape + '[m':
      item = None
    return item
