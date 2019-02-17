# `pycomment`

## Purpose
This is a `vi` command to comment or uncomment a section of Python code.

## Syntax
```
Syntax: pycomment
```

### Options and arguments
There are no options or arguments to the command itself.  However, its use requires you to be proficient in using `vi`, especially running commands and addressing a specific block of lines in the edit buffer.

## Example

### Before
Before invoking the command, consider that your edit buffer looks like:
```
0001 #! /usr/bin/env python
0002 
0003 import sys
0004
0005 print 'Before `if`'
0006 if len(sys.argv) > 1:
0007   """
0008     print the arguments
0009   """
0010   # here we go
0011   for num in range(1, len(sys.argv)):
0012     # this is a naive way to print a list
0013     print sys.argv[num]
0014   # # this is a better way to print a list
0015   # print '\n'.join(sys.argv[1:])
```
### Invoking the command
To comment out lines 11-13 and uncomment lines 14-15, you could use two `vi` commands:
```
:11,13!pycomment
:14,15!pycomment
```
### After
After the command runs, the comment status of lines 11 through 15 is swapped:
```
0001 #! /usr/bin/env python
0002 
0003 import sys
0004
0005 print 'Before `if`'
0006 if len(sys.argv) > 1:
0007   """
0008     print the arguments
0009   """"
0010   # here we go
0011   # for num in range(1, len(sys.argv)):
0012   # # this is a naive way to print a list
0013   #   print sys.argv[num]
0014   # this is a better way to print a list
0015   print '\n'.join(sys.argv[1:])
```

## Notes

- This was inspired by the [`Ctrl-/`](https://www.jetbrains.com/help/pycharm/commenting-and-uncommenting-blocks-of-code.html) command in [PyCharm](https://www.wikiwand.com/en/PyCharm).  I created this command because I often edit scripts just in `vi` rather than any IDE.