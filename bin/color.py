#! /usr/bin/env python

import re
import sys
import logging
import argparse

class Color(object):
  @staticmethod
  def get_color(arg):
    rets = {}

    log = logging.getLogger()

    log.debug('arg: {arg!r}'.format(**locals()))
    normalized_arg = re.sub(r'[-_ ]', '', arg).lower()
    log.debug('normalized_arg: {normalized_arg!r}'.format(**locals()))

    log.debug('colors: {Color.colors}'.format(**globals()))
    for (key, value) in Color.colors.items():
      log.debug('Testing {key!r}'.format(**locals()))
      if normalized_arg == key[:len(normalized_arg)]:
        rets[key] = value

    log.debug('normalized_arg: {normalized_arg!r}'.format(**locals()))

    if not rets:
      raise argparse.ArgumentTypeError('{arg!r} must be one of: {colors}'.format(
        arg=arg,
        colors=', '.join(Color.colors.keys())
      ))
    elif len(rets) > 1:
      raise argparse.ArgumentTypeError('{arg!r} is ambiguous: {colors}'.format(
        arg=arg,
        colors=', '.join(rets.keys())
      ))

    return rets.keys()[0]

  @staticmethod
  def print_color(color):
    if color:
      sys.stdout.write('\x1b[{}m'.format(Color.colors.get(color) or color))

  colors = {
    'black': '0;30',
    'white': '1;37',
    'red': '0;31',
    'blue': '0;34',
    'purple': '0;35',
    'cyan': '0;36',
    'orange': '0;33',
    'brown': '0;33',
    'green': '0;32',
    'yellow': '1;33',
    'darkgray': '1;30',
    'lightred': '1;31',
    'lightgreen': '1;32',
    'lightblue': '1;34',
    'lightpurple': '1;35',
    'lightcyan': '1;36',
    'lightgray': '0;37',
  }

if __name__ == '__main__':

  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  # log.setLevel(logging.DEBUG) # uncomment this to enable debugging in get_color() method

  parser = argparse.ArgumentParser(description='Print text in the specified color')
  parser.add_argument('color', type=Color.get_color,
                      help='Choose a color: {colors}'.format(colors=', '.join(Color.colors.keys())))
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  parser.add_argument('text', nargs='*', help='Text to display')

  args = parser.parse_args()

  log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  if args.text:
    Color.print_color(Color.get_color(args.color))
    sys.stdout.write(' '.join(args.text) + '\n')
    Color.print_color('0')
  else:
    if sys.stdin.isatty():
      parser.error('stdin must be redirected if text is not supplied on command line')
    Color.print_color(Color.get_color(args.color))
    sys.stdout.write(sys.stdin.read())
    if args.color:
      Color.print_color('0')
