# `grep-cat`

## Purpose
Display lines from a file based on regular expressions and line numbers.

## Syntax
```
Syntax: grep-cat [-h] [-i] [-n] [-f] [-v | -s] [-V] selector ... [file ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-i` `--ignore-case` | Perform case-insensitive searches | Regular expressions are case-sensitive |
| `-n` `--number` | Print line numbers | Line numbers are not printed |
| `-f` `--supress-file-names` | Supress file names | File names are printed when not reading from stdin |
| `-n` `--negate` | Print lines that do **not** match the selectors.  Mutually exclusive with `-s` | Lines are printed when they match the selectors |
| `-s` `--by-selectors` | Selectors are independent and all lines that a selector targets are printed before moving on to the next selector.  Mutually exclusive with `-n` | All selectors are processed before printing anything |
|  `-V`  | Enable verbose debugging.  Two or more instances generate more debugging | Debugging is not enabled |

### Selectors
Selectors are the logic by which the user selects what lines to include.  There are three types of selectors.
#### Line number selectors
A positive and negative integer can be used to select a line by its position in a file.  `1` is the first line, `-1` is the last line.
#### Regular expression selectors
A regular expression can be used to select lines by matching the 
expression.  The expression must be delimited by punctuation characters 
which do not appear in the regular expression.  For instance: `/foo-bar/`.
##### Regular expression offsets
A regular expression selector also accepts an "offset" of the form `+NUM` or `-NUM` to alter the selector to target lines before or after the the regular expression.

#### Range selectors
Two selectors (any combination of the previous selectors) can be combined using a colon between them to select a range 
of lines that begin with the first selector and end with the second selector.  For instance: `1:/foo/`.
##### Reference selectors
An additional selector available on either side _(but not both)_ of a range selector is a _reference selector_ of the form
`.+NUM` or `.-NUM`.  The period stands in for hits from the other selector allowing you to refer to lines relative
to the other selector.
##### Range selector logic
Here is how ranges involving regular expressions are processed:
1. All lines of a specified file are read
2. Regular expressions for the range selectors are processed against all lines
3. The number of starting selector lines must match the number of ending selector lines.  A warning is raised if not and the 
   processing for that range selector ends for that file. 
   
   Note that the number of matching lines from
   a line number selector is either one (the file has a line at the position) or zero (the file
   does not have a line at the position).  A regular expression selector can result in
   0 to many lines.
4. The ranges are a one-to-one match of starting selector lines to ending selector lines:
   1. The first range is the first line from the starting selector
   through the first line from the ending selector
   2. The second range is the second line from the starting selector
   through the second line of the ending selector
   3. etc. 


## Examples

### Basic examples
```
$ echo -e 'import string\nprint("\\n".join([c for c in string.ascii_lowercase[:10]]))' | python > foo.txt
$ cat -n foo.txt
     1	a
     2	b
     3	c
     4	d
     5	e
     6	f
     7	g
     8	h
     9	i
    10	j
$ grep-cat -n 1:2 -2:-1 foo.txt
foo.txt:1: a
foo.txt:2: b
foo.txt:9: i
foo.txt:10: j
$ grep-cat -n '/[ajz]/' foo.txt
foo.txt:1: a
foo.txt:10: j
$ grep-cat -vn '/[ajz]/' foo.txt
foo.txt:2: b
foo.txt:3: c
foo.txt:4: d
foo.txt:5: e
foo.txt:6: f
foo.txt:7: g
foo.txt:8: h
foo.txt:9: i
$ 
```
### Processing by selectors

By printing lines matching each selector first before moving on to the next selector, the tool can repeat a line:

```
$ df -h . | grep-cat -s 1:-1 1
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T   86G  1.8T   5% /media/mrbruno/ExtraDrive1
Filesystem      Size  Used Avail Use% Mounted on
$ 
```

### Regular expression offsets

```
$ cat test.txt
abc
def
ghi
jkl
mno
pqr
stu
vxy
z
$ grep-cat '/g/-1:/p/+1' test.txt
test.txt: def
test.txt: ghi
test.txt: jkl
test.txt: mno
test.txt: pqr
test.txt: stu
$ 
```

### Reference selector

```
$ cat test.txt
abc
def
ghi
jkl
mno
pqr
stu
vxy
z
$ grep-cat /g/:.+2 test.txt
test.txt: ghi
test.txt: jkl
test.txt: mno
$ 
```

## Notes

- In default selector mode, a selector that targets a line that was targetted by a previous selector will toggle its visibility.
For example, if the first selector makes line 1 visible but the second selector also selects line 1, the line becomes invisible. 
- Considering the previous note, overlapping ranges could result in undesirable results. For instance, consider this example:
    ```
    $ cat -n foo.txt
    1	aaa
    2	aaa
    3	zzz
    4	zzz
    $ grep-cat -n /aaa/ /zzz/ foo.txt
    foo.txt:1: aaa
    foo.txt:2: aaa
    foo.txt:3: zzz
    foo.txt:4: zzz
    $ grep-cat -n /aaa/-/zzz/ foo.txt
    foo.txt:1: aaa
    foo.txt:4: zzz
    $ 
    ```
    The first `grep-cat` command works as expected.  When combined in a range selector, the first set of matches toggles the state of
lines one through three, making them visible. But then the second group of matches toggles the state of lines two through four,
making lines two and three invisible, making four visible.

    Processing by selectors will generate different behavior:
    
    ```
    $ grep-cat -s -n /aaa/:/zzz/ foo.txt
    foo.txt:1: aaa
    foo.txt:2: aaa
    foo.txt:3: zzz
    foo.txt:2: aaa
    foo.txt:3: zzz
    foo.txt:4: zzz
    $ 
    ```

    I'm not wild about this behavior but I think this is a reasonable way to handle regular expressions especially with respect to 
overlapping ranges.  I reserve the right to change my mind.

- I bounded regular expression offsets and reference selectors by the number of lines in the file.
  - `.-1:1` is not invalid - the first selector would technically reference _line 0_ which doesn't exist but I made sure a reference never went below 1
  - `-1:.+1` is not invalid - the second selector would technically reference beyond the last line but I made sure a reference never goes beyond the last line

- `.+1:1` and `2:.-1` are probably both invalid because the first selector is greater than the second reference

- Initially I had designed range selectors to be delimited by a colon **or a hyphen** but once I introduced the ideas of reference selectors and regular expression offsets, I wanted to simplify the syntax and avoid ambiguities. 
   