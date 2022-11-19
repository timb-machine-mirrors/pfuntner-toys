# `wholegrep`

## Purpose
Show files that have:
- all desired regular expressions
- no undesired regular expressions

The regular expressions will match any occurrence in each file.

## Syntax
```
usage: wholegrep [-h] [-v] [-a] [--ignorecase]
                 [-i INCLUDE] [-i INCLUDE] ...
                 [-x EXCLUDE] [-x EXCLUDE] ...
                 file [file ...]
positional arguments:
  file                  One or more files to scan

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable debugging
  -a, --all             Report on all files
  -i INCLUDE, --include INCLUDE
                        Specify a required regular expression
  -x EXCLUDE, --exclude EXCLUDE
                        Specify an undesireable regular expression
  --ignorecase          Treat all regular expressions as case insensitive
```

The names of one or more files can be specified.

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-a` or `--all` | Show search status of all files.  When specified, each file is printed with a `+` (_pass_) or `-` (_fail_) preceding the file. | The default is to only print files that satisify the requirements. |
| `--ignorecase` | Ignore case for all regular expressions | The default is to respect case in all regular expressions |
| `-i INCLUDE` or `--include INCLUDE` | Specify a regular expression that the files must possess.  Zero or more regular expressions can be specified. | The default is to not require any regular expressions |
| `-x EXCLUDE` or `--exclude EXCLUDE` | Specify a regular expression that the files must not possess.  Zero or more regular expressions can be specified. | The default is to not restrict any regular expressions |
| `-v` | Enable verbose debugging | Debugging is not enabled |

## Examples

```
$ wholegrep -i import\ argparse bin/* | headtail
       1 bin/abspath
       2 bin/acp
       3 bin/aliasgrep
       4 bin/allcommits
       5 bin/anonymize
         .
         .
         .
      87 bin/viswap
      88 bin/whatami
      89 bin/wholegrep
      90 bin/xml
      91 bin/yaml
$ wholegrep -i import\ argparse bin/* -x import\ logging | headtail
       1 bin/abspath
       2 bin/indent
       3 bin/jsondiff
       4 bin/math
       5 bin/timestamps
$ wholegrep -a -i sys.argv bin/* | headtail -30
       1 - bin/abspath
       2 - bin/acp
       3 + bin/addcrs
       4 - bin/aliasgrep
       5 - bin/allcommits
       6 - bin/anonymize
       7 - bin/ansible2json
       8 - bin/append
       9 - bin/assassinate
      10 - bin/autoscp
      11 + bin/backup
      12 - bin/badimport
      13 - bin/banner
      14 + bin/bashprofiles
      15 + bin/basicfy
         .
         .
         .
     258 + bin/watcher
     259 + bin/wcsum
     260 + bin/webwatch
     261 + bin/whatami
     262 + bin/whatfile
     263 + bin/whatgit
     264 - bin/whatpython
     265 - bin/whatshell
     266 + bin/whochat
     267 - bin/wholegrep
     268 - bin/xml
     269 - bin/yaml
     270 - bin/ymd
     271 - bin/zerojoin
     272 - bin/zombies
$
```

## Notes

- At least one regular expression (either `--include` or `--exclude`) must be specified but any combination is allowed.
