# `ssh-exec`

## Purpose
Execute a script on a remote host.

## Syntax
```
Syntax: ssh-exec [--verbose] [-i INTERPRETER ...] [-d] [-q] [-b] [-e ENV] [-v] host script [arg [arg ...]]
```

### Options and arguments
| Option                            | Description                                                                                                                           | Default                                                                        |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `-i`, `--interpreter`             | Run the script with a specific interpeter.  Arguments can be specified in the same argument.                                          | The remote host detects the interpreter, possibly through bang-slash comment   |
| `-d`, `--docker`                  | Treat remote host as a Docker container                                                                                               | `ssh` is used to access the remote host                                        |
| `-q`, `--quiet`                   | Uses the `ssh --quiet` option.  Not applicable with `--docker`                                                                        | Extra messages may come from `ssh`                                             |
| `-e key=value`, `--env key-value` | Defines an environment variable and value to be used while the script runs.  Multiple occurrences can be used for multiple variables. | No extra environment variables are used                                        |
| `-b`, `--become`                  | Use `sudo` on the remote host to become root before running script                                                                   | root it not used - an unprivileged user is likely used                         |
| `-v`, `--verbose`                 | Enable verbose debugging                                                                                                              | Debugging is not enabled                                                       |

## Example

#### Bash script
Here's a sample Bash script with which I'll demonstrate:
```commandline
$ cat ~/tmp/HelloWorld.sh
#! /usr/bin/env bash

echo "Hello, uid $(id -u) from bash world"
echo
echo "Number of arguments: $#"
curr=1
while [ $# -gt 0 ]
do
  echo "$curr: $1"
  shift 1
  let 'curr=curr+1'
done

if env | grep -q ^FOO
then
  echo
  env | grep ^FOO
fi
$
```
##### `ssh` examples
```commandline
$ ssh-exec -e FOO=bar localhost ~/tmp/HelloWorld.sh 1 2 3
Hello, uid 1000 from bash world

Number of arguments: 3
1: 1
2: 2
3: 3

FOO=bar
$ ssh-exec -b -e FOO=bar localhost ~/tmp/HelloWorld.sh 1 2 3
Hello, uid 0 from bash world

Number of arguments: 3
1: 1
2: 2
3: 3

FOO=bar
$ ssh-exec -i 'bash -x' -e FOO=bar localhost ~/tmp/HelloWorld.sh 1 2 3
++ id -u
Hello, uid 1000 from bash world

+ echo 'Hello, uid 1000 from bash world'
+ echo
Number of arguments: 3
+ echo 'Number of arguments: 3'
+ curr=1
+ '[' 3 -gt 0 ']'
1: 1
+ echo '1: 1'
+ shift 1
+ let curr=curr+1
+ '[' 2 -gt 0 ']'
+ echo '2: 2'
2: 2
+ shift 1
+ let curr=curr+1
+ '[' 1 -gt 0 ']'
+ echo '3: 3'
3: 3
+ shift 1
+ let curr=curr+1
+ '[' 0 -gt 0 ']'
+ env
+ grep -q '^FOO'

+ echo
+ env
+ grep '^FOO'
FOO=bar
$ 
```

##### Docker example
I'm using an Alpine container which doesn't come with a `bash` interpreter so I'll override the _slash-bang_ comment:
```commandline
$ ssh-exec -i sh -e FOO=bar -d alpine ~/tmp/HelloWorld.sh 1 2 3
Hello, uid 0 from bash world

Number of arguments: 3
1: 1
2: 2
3: 3

FOO=bar
$ 
```

```commandline
$ ssh-exec -e FOO=bar localhost ~/tmp/HelloWorld.sh 1 2 3
Hello, uid 1000 from bash world

Number of arguments: 3
1: 1
2: 2
3: 3

FOO=bar
$ ssh-exec -b -e FOO=bar localhost ~/tmp/HelloWorld.sh 1 2 3
Hello, uid 0 from bash world

Number of arguments: 3
1: 1
2: 2
3: 3

FOO=bar
$ 
```

#### Python script
Here's a sample Python script with which I'll demonstrate:
```
$ cat ~/tmp/HelloWorld.py
#! /usr/bin/env python

import os
import sys

print(f'Hello uid {os.getuid()}, Python world\n')

print(f'Number of arguments: {len(sys.argv)-1}')
for arg in range(1, len(sys.argv)):
  print(f'{arg}: {sys.argv[arg]!r}')

foo_env = {key:os.environ[key] for key in os.environ.keys() if key.startswith('FOO')}
if foo_env:
  print()
  for (key, value) in foo_env.items():
    print(f'{key}={value!r}')
$ 
```
##### Example
```commandline
$ ssh-exec localhost ~/tmp/HelloWorld.py
Hello uid 1000, Python world

Number of arguments: 0
$ 
```

## Notes

- The script is most effective with `ssh` hosts if you enable password-less `ssh` using keys 
