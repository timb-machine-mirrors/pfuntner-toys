# `capture`

## Purpose
Capture output and other info from a shell command:

  - saves stdout and stderr to a file
  - print:
    - start and stop time, duration
    - exit status
    - if the command was killed by a signal, the signal number and symbolic name
    - user and system CPU time

## Syntax
```
Syntax: capture [-o | --output FILENAME] command [OPTIONS ...] [ARGUMENTS ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-o` or `--output`  | Specify output file nameor directory | `./{commandBaseName}-%Y%m%d%H%M%S%f.out` |

## Example

```
$ capture python -c 'for num in range(10): print num'
Writing to 'capture-20180418152936235508.out'
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

Start: 2018-04-18T15:29:36.243807
Stop: 2018-04-18T15:29:36.409296
Duration: 0:00:00.165489
Status: 0000, rc=0
User: 0.05s, System: 0.11s
$ headtail capture-20180418152936235508.out
capture-20180418152936235508.out        1 0
capture-20180418152936235508.out        2 1
capture-20180418152936235508.out        3 2
capture-20180418152936235508.out        4 3
capture-20180418152936235508.out        5 4
                                          .
                                          .
                                          .
capture-20180418152936235508.out       12 Start: 2018-04-18T15:29:36.243807
capture-20180418152936235508.out       13 Stop: 2018-04-18T15:29:36.409296
capture-20180418152936235508.out       14 Duration: 0:00:00.165489
capture-20180418152936235508.out       15 Status: 0000, rc=0
capture-20180418152936235508.out       16 User: 0.05s, System: 0.11s

$
```

## Notes

- If the command is a script (Bash, Python, awk, etc.), you will likely have to invoke the interpreter and give it the script file name.
- If you just specify a directory for `-o` and don't specify a file name, the default file name will be created in the specified directory
