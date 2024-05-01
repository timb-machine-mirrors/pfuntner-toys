#! /usr/bin/env python3

import re
import sys
import string
import logging
import argparse

parser = argparse.ArgumentParser(description='Anonymize stdin data')

group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--digits', action='store_true', help='Remove only decimal digits')
group.add_argument('-x', '--hexadecimal', action='store_true', help='Remove only hexadecimal digits')

args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if sys.stdin.isatty():
  parser.error('stdin must be redirected')

if args.digits:
  regexp = re.compile(r'\d+')
elif args.hexadecimal:
  regexp = re.compile(r'([0-9][0-9a-fA-F]*)|([0-9a-fA-F]*[0-9])|([0-9a-fA-F]*[0-9][0-9a-fA-F]*)')
else:
  regexp = re.compile(r'\w+')

calendar_words = re.compile('(jan(unary)?)|(feb(ruary)?)|(mar(ch)?)|(apr(il)?)|may|(jun(e)?)|(jul(y)?)|(aug(ust)?)|(sep(tember)?)|(oct(ober)?)|(nov(ember)?)|(dec(ember)?)|((sun|mon|tue(s)?|wed(nes)?|thu(rs)?|fri|sat(ur)?)(day)?)', flags=re.IGNORECASE)

unprintables = re.compile(f'[^{string.printable}]')
while True:
  line = sys.stdin.readline()
  if line:
    line = regexp.sub('#' if (args.digits or args.hexadecimal) else 'foo', line)
    line = unprintables.sub('', line)
    line = calendar_words.sub('foo', line)
    sys.stdout.write(line)
  else:
    break
