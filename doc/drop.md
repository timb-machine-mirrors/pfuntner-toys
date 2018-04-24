# `drop`

## Purpose
Drop a number of lines from stdin or from one or more files.  This sort of the reverse of the standard `head` and `tail` utilities except it discards the "head"/"tail" instead of only returning them.

## Syntax
```
Syntax: head [num | -num] [file ...]
```

### Options and arguments
- The first argument must be a positive or negative integer (let's call it `n`).  Positive values discard the top `n` lines and negative values discard the bottom `n` lines.
- The number of lines can be followed by one or more files.

## Example

```
$ python -c 'print "\n".join([str(num) for num in range(100)])' | wc
    100     100     290
$ python -c 'print "\n".join([str(num) for num in range(100)])' | drop 90
90
91
92
93
94
95
96
97
98
99
$ python -c 'print "\n".join([str(num) for num in range(100)])' | drop -90
0
1
2
3
4
5
6
7
8
9
$
$ drop 95 <(python -c 'print "\n".join([str(num) for num in range(100)])')
95
96
97
98
99

$ ls -l
total 56
-rwxr-xr-x  1 jpfuntne Domain Users    0 Mar 21 14:01 __init__.py
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Apr 24 13:42 bin
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Apr 24 13:53 doc
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Feb  7 13:15 misc
-rw-r--r--  1 jpfuntne Domain Users 2765 Apr 24 13:52 README.md
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Mar 22 13:56 test
$ ls -l | drop 1
-rwxr-xr-x  1 jpfuntne Domain Users    0 Mar 21 14:01 __init__.py
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Apr 24 13:42 bin
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Apr 24 13:53 doc
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Feb  7 13:15 misc
-rw-r--r--  1 jpfuntne Domain Users 2765 Apr 24 13:52 README.md
drwxr-xr-x+ 1 jpfuntne Domain Users    0 Mar 22 13:56 test
$
```

## Notes

- If no files are specified, the command reads from stdin if it is redirected.  Is is an error to not specify a filename and not redirect stdin.
- This can be very useful when you wish to discard the header of output (see the `ls` example above).
