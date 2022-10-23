# `strip-trailing-whitespace`

## Purpose
Strip trailing whitespace in one or more files

## Syntax
```
Syntax: strip-trailing-whitespace [-h] [--dry-run] [-l] [-v] [file [file ...]]
```

### Options and arguments
| Option            | Description                         | Default                             |
|-------------------|-------------------------------------|-------------------------------------|
| `-d`, `--dry-run` | Examines files but makes no changes | Makes changes to files as necessary |
| `-l`, `--long`    | Prints lines that need changes      | Only a summary of files is printed  |
| `-v`              | Enable verbose debugging            | Debugging is not enabled            |

## Examples

I'll use a rather complicated `find` command to generate the files for the script to act upon.  I am excluding some files that have non-printable characters:

```commandline
$ find ~/bin -follow ! -name \*.class ! -name \*.deb ! -name \*.pyc -type f -print0 | xargs -r0 strip-trailing-whitespace --dry 
2022-10-23 14:10:14,960 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/table.py: 959 total lines, 4 lines with trailing whitespace
2022-10-23 14:10:14,960 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/acp: 79 total lines, 0 lines with trailing whitespace
2022-10-23 14:10:14,960 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/recentdownloads: 71 total lines, 1 lines with trailing whitespace
.
.
.
2022-10-23 14:10:15,039 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/findmetrics: 137 total lines, 1 lines with trailing whitespace
2022-10-23 14:10:15,039 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/seejson: 72 total lines, 2 lines with trailing whitespace
2022-10-23 14:10:15,039 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/columns: 145 total lines, 1 lines with trailing whitespace
$ 
```

```commandline
$ find ~/bin -follow ! -name \*.class ! -name \*.deb ! -name \*.pyc -type f -print0 | xargs -r0 strip-trailing-whitespace --long
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/table.py: 959 total lines, 4 lines with trailing whitespace
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/table.py:523: '      the end of a column where the same position is whitespace on all of the lines. '
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/table.py:525: '  '
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/table.py:537: '  '
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/table.py:732: "    This method performs the same function as add().  I added it because I can't "
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/acp: 79 total lines, 0 lines with trailing whitespace
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/recentdownloads: 71 total lines, 1 lines with trailing whitespace
2022-10-23 14:12:03,819 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/recentdownloads:23: '  '
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/dates: 94 total lines, 1 lines with trailing whitespace
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/dates:78: '  '
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/BrunoUtils.py: 267 total lines, 12 lines with trailing whitespace
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/BrunoUtils.py:15: '    '
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/BrunoUtils.py:19: '    '
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/BrunoUtils.py:24: '    '
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/BrunoUtils.py:29: '    '
2022-10-23 14:12:03,820 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/BrunoUtils.py:94: '  '
.
.
.
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/windoze-screensavers: 57 total lines, 0 lines with trailing whitespace
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/tabular: 130 total lines, 0 lines with trailing whitespace
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/findmetrics: 137 total lines, 1 lines with trailing whitespace
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/findmetrics:108: '    '
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/seejson: 72 total lines, 2 lines with trailing whitespace
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/seejson:32: '         '
2022-10-23 14:12:04,243 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/seejson:34: '  '
2022-10-23 14:12:04,244 INFO /home/mrbruno/bin/strip-trailing-whitespace:27 /home/mrbruno/bin/columns: 145 total lines, 1 lines with trailing whitespace
2022-10-23 14:12:04,244 INFO /home/mrbruno/bin/strip-trailing-whitespace:30   /home/mrbruno/bin/columns:137: '  '
$ 
```

## Notes

- If no files are specified, the script will read from stdin and write the updated lines to stdout
- The script is not designed for binary files but it does pass over them without much fuss.