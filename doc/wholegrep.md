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
| `-a` or `--all` | Show search status of all files | The default is to only print files that satisify the requirements. |
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
$ 
```

## Notes

- At least one regular expression (either `--include` or `--exclude`) must be specified but any combination is allowed.
