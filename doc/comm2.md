# `comm2`

## Purpose
This was inspired by the standard `comm` Unix utility.  I was using it one day to compare a couple of files but grew dissatisfied because it requires that the input files are sorted.  This script **does not**.  It simply compares the files as-is without assuming that they're sorted.

## Syntax
```
Syntax: comm2 [-123] [--json] file1 file2
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-1`  | Eliminate lines unique to `file1` | The default is to print all lines |
|  `-2`  | Eliminate lines unique to `file2` | The default is to print all lines |
|  `-3`  | Eliminate lines unique to both files | The default is to print all lines |
|  `--json`  | Print results in JSON format | The default is to lines with minimal formatting, only separating the three categories by a tab character. |

## Example

```
$ comm2 <(echo -e one\\ntwo) <(echo -e two\\nthree)
	one
two
		three
$ comm2 <(echo -e one\\ntwo) <(echo -e two\\nthree) | cat -A
^Ione$
two$
^I^Ithree$
$ comm2 -12 <(echo -e one\\ntwo) <(echo -e two\\nthree)
two
$ comm2 -12 --json <(echo -e one\\ntwo) <(echo -e two\\nthree)
[
  {
    "line": "two",
    "pos1": 2,
    "pos2": 1,
    "status": "common"
  }
]
$
```

## Notes

- The minimal formatting output makes use of tab characters to separate lines belonging to different categories:
  - Unless eliminated, a line appearing in the first tab-delimited field was unique to `file1`
  - Unless eliminated, a line appearing in the second tab-delimited field was unique to `file2`
  - Unless eliminated, a line appearing in the third tab-delimited field was common to both files.
  - If `-1`, `-2`, or `-3` is specified, there will be fewer fields in the output.  For instance if `-1` is specified but `-2` is not, lines unique to `file2` will appear as the first field in the output, not the second.
- Two file names must be specified.  Note the command substitution technique used in the example:

  ```
  $ foo ... <(bar ...)  ...
  ```

  If your input comes from a command or pipeline, you could use the same technique where the shell writes the data to a temporary file and passes the filename as an argument to `comm2`.  All `comm2` sees is a filename - it has no idea that command substitution was performed.
- Using the regular `comm` with one of these above examples:

  ```
  $ comm <(echo -e one\\ntwo) <(echo -e two\\nthree)
  one
		two
  comm: file 2 is not in sorted order
	three
  $

  ```

  The behavior is is pretty much as expected and the error message can easily be disposed of but I'm not convinced that more complicated examples will work as well.  If I come up with a more complicated example that demostrates the benefit of my script, I'll share it.
