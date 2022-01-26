#! /usr/bin/env python3

import sys
import json
import signal
import logging
import argparse

from html.parser import HTMLParser
import xml.etree.ElementTree as ET

class LazyHtml(object):
  """
    This outer class is the interface we expect callers to use:

      parser = LazyHtml(log)
      root = parser.parse(html_string)
  """

  class Node(object):
    """
      Helper class to represent a node in an HTML tree.

      We don't expect the caller to reference this class to it's an inner class of LazyHtml.
    """
    def __init__(self, tag, attrs):
      self.path = None
      self.tag = tag
      self.attrs = attrs
      self.children = list()
      self.text = None
      self.tail = None

    def __str__(self):
      return f'<{self.tag} {self.attrs}/>'

  class BaseLazyHtmlParser(HTMLParser):
    """
      Helper class which extends the base HTMLParser class to forgive common HTML errors
      such as neglecting to close tags that prevents the source from being parsed as XHTML.

      We don't expect the caller to reference this class to it's an inner class of LazyHtml.
    """
    def __init__(self, log):
      self.root = None
      self.log = log
      self.stack = list()
      super().__init__()

    def handle_starttag(self, tag, attrs):
      """
        Remember a new tag
      """
      self.log.debug(f'Encountered a <{tag}>')
      node = LazyHtml.Node(tag, attrs)
      if self.root is None:
        self.root = node
      else:
        self.stack[-1].children.append(node)
      self.stack.append(node)
      node.path = '/' + '/'.join([stack_node.tag for stack_node in self.stack])

    def handle_endtag(self, tag):
      """
        Finish a tag - we will forgive if the "current" node is not the one being closed... We'll work our way
        up the stack to find the LAST node that matches the tag being closed.

        It is an error if there are no open nodes matching the tag being closed.
      """
      self.log.debug(f'Encountered a </{tag}>')

      if tag not in [node.tag for node in self.stack]:
        self.log.error(f'Encountered unmatched </{tag}>')
        exit(1)

      while self.stack and self.stack[-1].tag != tag:
        self.log.debug(f'Encountered </{tag}> but expected </{self.stack[-1].tag}> first')
        self.stack.pop()

      self.stack.pop()

    def handle_data(self, data):
      """
        Add data to a node.

        It is an error if we read non-whitespace data without an open node.
      """
      self.log.debug(f'Encountered data {data!r}')
      if self.stack:
        self.stack[-1].children.append(data.strip())
      elif not data.strip():
        self.log.debug('Ignoring whitespace without a node')
      else:
        self.log.error(f'Encountered data {data!r} without a node')
        exit(1)

  def __init__(self, log=None):
    if log:
      self.log = log
    else:
      logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
      self.log = logging.getLogger()

    self.parser = self.BaseLazyHtmlParser(self.log)

  def get_root(self, html):
    self.parser.feed(html)
    return self.parser.root

  def parse(self, html):
    root = self.get_root(html)
    self.normalize_strings(root)
    return self.to_xml(root)

  @staticmethod
  def get_attrs(tuples):
    return {name:value for (name, value) in tuples}

  def to_json(self, node):
    ret = None
    if node:
      if isinstance(node, str):
        return node
      else:
        ret = {'tag': node.tag, 'attrs': self.get_attrs(node.attrs), 'children': [], 'path': node.path}
        for child in node.children:
          ret['children'].append(self.to_json(child))
    return ret

  def normalize_strings(self, node):
    """
      Prepare a tree for XML by moving string nodes to either:
        - parent.text if the string node is the first node of the children of the parent
        - older_sibling.tail if the string node is not the first node of the children of the parent
    """
    if node:
      pos = 0
      if node.children:
        if isinstance(node.children[0], str):
          self.log.debug(f'{node.tag} text: {node.children[0]!r}')
          node.text = node.children.pop(0)
        else:
          self.normalize_strings(node.children[0])
          pos += 1

      while pos < len(node.children):
        if isinstance(node.children[pos], str):
          self.log.debug(f'{node.tag} tail: {node.children[pos]!r}')
          node.children[pos-1].tail = node.children.pop(pos)
        else:
          self.normalize_strings(node.children[pos])
          pos += 1

  def to_xml(self, node, parent=None):
    params = {'attrib': self.get_attrs(node.attrs)}
    xml_node = ET.Element(node.tag, **params) if parent is None else ET.SubElement(parent, node.tag, **params)
    if node.text:
      xml_node.text = node.text
    if node.tail:
      xml_node.tail = node.tail

    for child in node.children:
      self.to_xml(child, xml_node)
    return xml_node

def visit(node, indent=0):
  if node:
    if isinstance(node, str):
      print(f'{" " * (indent*2)}{node}')
    else:
      attrs = (' ' + ' '.join([f'{name}={value!r}' for (name, value) in html_parser.get_attrs(node.attrs).items()])) if node.attrs else ''

      print(f'{" " * (indent*2)}<{node.tag}{attrs}>')
      for child in node.children:
        visit(child, indent+1)
      print(f'{" " * (indent*2)}</{node.tag}>')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=sys.argv[0])

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-j', '--json', action='store_true', help='Generate JSON output')
  group.add_argument('-x', '--xml', action='store_true', help='Generate XML output')

  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  args = parser.parse_args()

  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  log.setLevel(logging.WARNING - (args.verbose or 0)*10)

  signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

  if sys.stdin.isatty():
    parser.error('stdin must be redirected')

  html_parser = LazyHtml(log)
  root = html_parser.get_root(sys.stdin.read())

  if args.json:
    json.dump(html_parser.to_json(root), sys.stdout)
  elif args.xml:
    html_parser.normalize_strings(root)
    ET.dump(html_parser.to_xml(root))
  else:
    visit(root)
