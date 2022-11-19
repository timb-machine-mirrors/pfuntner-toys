#! /usr/bin/env python3
import re
import sys
import signal
import logging
import argparse
import requests
import subprocess

from lxml import html


class Table(object):
  def __init__(self, *args):
    if len(args) == 1 and type(args[0]) in (list, tuple):
      self.headings = args[0]
    else:
      self.headings = args

    try:
      self.p = subprocess.Popen(['column', '-t', '-s\t'], stdin=subprocess.PIPE, text=True)
    except Exception as e:
      log.error(f'Error opening `column`: {e!s}. On Ubuntu, try installing the bsdmainutils package')
      exit(1)

    self.p.stdin.write('\t'.join([str(heading) for heading in self.headings]) + '\n')

  def add(self, *args):
    self.p.stdin.write('\t'.join([str(arg) for arg in args]) + '\n')

  def close(self):
    self.p.stdin.close()
    self.p.wait()


def visit(root, indent=0):
  """
  Print a tree to stdout (primarily for diagnostic purposes).  It's also an excellent example of visiting all nodes in a tree

  :param root: The top xlml Element to print
  :param indent: The depth of the call stack, indicates how far to indent the root node
  :return: None
  """
  print(f'{" "*(indent*2)}<{root.tag}{" " + (" ".join([f"{key}={value!r}" for (key,value) in root.attrib.items()])) if root.attrib else ""}>{(root.text or "").strip()}')
  for node in root:
    visit(node, indent+1)
  print(f'{" "*(indent*2)}</{root.tag}>{(root.tail or "").strip()}')


def find(root, tag=None):
  """
  Recursively locate elements which match the criteria.

  :param root: The top xlml Element to examine
  :param tag: The desired tag of nodes to return
  :return: A list of xlml Elements which satisfy the criteria
  """
  ret = list()
  if tag is not None and root.tag == tag:
    ret.append(root)
  for node in root:
    ret += find(node, tag=tag)
  return ret


def append(l, s):
  """
  Append a string to a list of strings

  :param l: A list of strings
  :param s: Potential string or None
  :return: None
  """
  s = (s or '').strip()
  if s:
    l.append(s)


def text(root, level=0):
  """
  Recursively collect all text of the root and all children.

  :param root: The top xlml Element to examine
  :param level: Indicates call stack depth
  :return:
    The method returns all text of root with all text of its children
    When level = 0 (the default): A single string containing all text concatenated together with blanks
    When level != 0: A list of strings coming from inside or after various elements
  """
  ret = list()
  append(ret, root.text)
  for node in root:
    ret += text(node, level+1)
  append(ret, root.tail)
  if level == 0:
    # join list of strings together into a single string
    ret = ' '.join(ret)
  return ret


def last_status(s):
  return dot_regexp.split(s)[-1]

parser = argparse.ArgumentParser(description='Parse DOJ January 6th suspects')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

aka_regexp = re.compile(r'\s*\(aka\b.*$')
dot_regexp = re.compile(r'\.\s+')

url = 'https://www.justice.gov/usao-dc/capitol-breach-cases'
req = requests.get(url)
if req.ok:
  root = html.fromstring(req.text)
  tables = find(root, 'table')
  if len(tables) == 1:
    table = tables[0]
    rows = find(table, 'tr')
    log.info(f'{len(rows)} rows found')
    headings = list()
    heading_cells = rows[0]
    for cell in find(heading_cells, 'th'):
      headings.append(text(cell))
    log.info(f'Headings are: {list(enumerate(headings))}')

    """
    Each suspect looks like:
      Index  Key                  Value
      0      Case Number          1:21-cr-212
      1      Name                 ADAMS, Jared Hunter
      2      Charge(s)            Entering and Remaining in a Restricted Building; Disorderly and Disruptive Conduct in a Restricted Building; Violent Entry and Disorderly Conduct in a Capitol Building; Parading, Demonstrating, or Picketing in a Capitol Building
      3      Case Documents       Adams & Jared - Information Adams & Jared - Statement of Facts Adams & Jared - Complaint
      4      Location of Arrest   OHIO, Hilliard
      5      Case Status          Arrested 3/9/2021. Charged via criminal information on 3/11/21. Arraignment and status conference held 5/4 and pleaded not guilty to all counts. Defendant remains on personal recognizance bond.
      6      Entry Last Updated*  December 15, 2021
    """
    table = Table('Name', 'Updated', 'Status')
    for suspect in rows[1:]:
      cells = [text(cell) for cell in find(suspect, 'td')]
      table.add(aka_regexp.sub('', cells[1]), cells[6], last_status(cells[5]))
    table.close()
  else:
    log.error('{count(tables)} tables found')
    exit(1)
else:
  log.fatal(f'{url!r} failed: {req.status_code}: {req.text!r}')
  exit(1)
