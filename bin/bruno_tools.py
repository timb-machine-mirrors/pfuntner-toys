#! /usr/bin/env python3

import shlex
import subprocess

def run(cmd, stdin=None, capture=True, shell=False, log=None):
  if shell:
    if isinstance(cmd, list):
      cmd = shlex.join(cmd)
  elif isinstance(cmd, str):
    cmd = cmd.split()

  if log:
    log.info('Executing {cmd}'.format(**locals()))

  p = None
  try:
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE if stdin else None, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None, shell=shell)
  except Exception as e:
    (rc, stdout, stderr) = (-1, '', f'Caught {e!s} running {cmd!r}')

  if p:
    if stdin:
      p.stdin.write(stdin.encode())
      p.stdin.close()
    if capture:
      (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
    else:
      (stdout, stderr) = ('', '')
    rc = p.wait()

  if log:
    log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

class Table(object):
    """
    A class the produces pretty tabular output - nicely alinged rows and columns
    """
    def __init__(self, *headings, banner=False):
        """
        Constructor that initializes the Table class

        Args:
            headings: A list of objects for the headings of the columns.  The number
            of headings must match the number of cells in each row.
        """
        # `self.data` is a list that contains all the cells in the table, including the headings
        self.data = [ [str(heading) for heading in headings] ]

        # `self.widths` contains the widths of each column - the maximum width of each cell in a column
        self.widths = [len(heading) for heading in self.data[0]]

        if banner:
          self.banner = '=' if banner == True else banner
        else:
          self.banner = False


    def add(self, *columns):
        """
        Adds a row to the table

        Args:
            columns: A list of objects for the cells in the row.
        """

        # assure the number of cells matches the number of headings
        assert len(columns) == len(self.data[0])

        self.data.append(list(map(str, columns)))

        # recalculate the maximum columns widths
        for (column_number, column) in enumerate(self.data[-1]):
            self.widths[column_number] = max(self.widths[column_number], len(column))

    def __str__(self):
        """
        Formats the rows (including headings) and columns aligned according to
        the maximum width of each column
        """
        ret = list()

        if self.banner:
          self.data.insert(1, [self.banner * self.widths[col_num] for col_num in range(len(self.data[0]))])
          self.banner = False

        for row_num in range(len(self.data)):
            ret.append(('  '.join([self.data[row_num][col_num].ljust(self.widths[col_num]) for col_num in range(len(self.data[0]))])).rstrip())

        return '\n'.join(ret)

    def close(self):
        """
        Completes the table and prints out all the rows (including headings) and columns aligned according to
        the maximum width of each column
        """

        print(str(self))

if __name__ == '__main__':
  import sys

  print(f'{sys.argv[0]!r} is designed to be imported into other scripts and not run independently')
  exit(1)
