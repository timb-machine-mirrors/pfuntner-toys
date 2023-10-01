#! /usr/bin/env python3

import re
import sys
import logging
import argparse

from table import Table

class Color(object):
  @staticmethod
  def get_color(arg):
    rets = {}

    log = logging.getLogger()

    log.debug('arg: {arg!r}'.format(**locals()))
    normalized_arg = re.sub(r'[-_ ]', '', arg).lower().replace('grey', 'gray')
    log.debug('normalized_arg: {normalized_arg!r}'.format(**locals()))

    log.debug('colors: {Color.color_codes}'.format(**globals()))
    for (key, value) in Color.color_codes.items():
      log.debug('Testing {key!r}'.format(**locals()))
      if normalized_arg == key[:len(normalized_arg)]:
        rets[key] = value

    log.debug('normalized_arg: {normalized_arg!r}'.format(**locals()))

    if not rets:
      raise argparse.ArgumentTypeError('{arg!r} must be one of: {colors}'.format(
        arg=arg,
        colors=', '.join(Color.color_codes.keys())
      ))
    elif len(rets) > 1:
      raise argparse.ArgumentTypeError('{arg!r} is ambiguous: {colors}'.format(
        arg=arg,
        colors=', '.join(rets.keys())
      ))

    return list(rets.keys())[0]

  @staticmethod
  def get_color_escape_code(color, background_color=None):
    return ('\x1b[{}m'.format(Color.get_color_code(color) or color) if color else '') + \
           ('\x1b[{}m'.format(Color.get_color_code(background_color) + 10) if background_color else '')

  @staticmethod
  def print_color(color, background_color=None):
    if color:
      sys.stdout.write(Color.get_color_escape_code(color, background_color))

  @classmethod
  def get_color_code(cls, color_name):
    return cls.color_codes.get(color_name)

  """
    I don't know where I got the color codes from originally but
    https://www.codeproject.com/Articles/5329247/How-to-Change-Text-Color-in-a-Linux-Terminal
    seems to make more sense and guides me for doing foreground
    and background colors.  The codes below are all foreground -
    you can just add 10 to any code to get the background code.
  """
  color_codes = {
    'default':     29,
    'black':       30,
    'darkred':     31,
    'darkgreen':   32,
    'darkyellow':  33,
    'darkblue':    34,
    'darkmagenta': 35,
    'darkcyan':    36,
    'lightgray':   37,
    'darkgray':    90,
    'red':         91,
    'green':       92,
    'orange':      93,
    'blue':        94,
    'magenta':     95,
    'cyan':        96,
    'white':       97,
  }

if __name__ == '__main__':

  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log = logging.getLogger()
  # log.setLevel(logging.DEBUG) # uncomment this to enable debugging in get_color() method

  parser = argparse.ArgumentParser(description='Print text in the specified color')

  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('color', type=Color.get_color, nargs='?',
                     help='Choose a foreground color: {colors}'.format(colors=', '.join(Color.color_codes.keys())))
  group.add_argument('--test', action='store_true', required=False, help='Test all colors')
  group.add_argument('-r', '--reset', action='store_true', help='Reset a console to default color only')

  parser.add_argument('-b', '--background-color', type=Color.get_color,
                      help='Choose a background color: {colors}'.format(colors=', '.join(Color.color_codes.keys())))

  parser.add_argument('-p', '--persist', action='store_true', help='Set a console to the specified color')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  parser.add_argument('text', nargs='*', help='Text to display')

  args = parser.parse_args()

  if (args.reset or args.test) and args.text:
    parser.error('--test and --reset are mutually exclusive with text')

  if (args.reset or args.test or args.text) and args.persist:
    parser.error('--test, --reset, and text are mutually exclusive with --persist')

  if args.persist and not(args.color):
    parser.error('color is required with --persist')

  log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  if args.reset:
    Color.print_color('0')
    Color.print_color('10')
  elif args.test:
    table = Table([])
    for color in Color.color_codes.keys():
      table.add(color, Color.get_color_escape_code(color) + color + Color.get_color_escape_code('0') + Color.get_color_escape_code('10'))
    print(str(table))
  elif args.text:
    Color.print_color(Color.get_color(args.color), args.background_color if args.background_color else None)
    sys.stdout.write(' '.join(args.text) + '\n')
    Color.print_color('0')
    Color.print_color('10')
  elif args.persist:
    Color.print_color(Color.get_color(args.color), args.background_color if args.background_color else None)
    print('')
  else:
    if sys.stdin.isatty():
      parser.error('stdin must be redirected if text is not supplied on command line')
    Color.print_color(Color.get_color(args.color), args.background_color if args.background_color else None)
    sys.stdout.write(sys.stdin.read())
    if args.color:
      Color.print_color('0')
      Color.print_color('10')
