# `versions`

## Purpose
Show versions of arbitrary commands.

## Syntax
```
Syntax: versions [-d | --version] [-v] target [target ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-d`, `--dumb` | Do not try to parse out version | Attempts are made to parse out the version.  See the examples |
| `--version` | Print out only version - only one argument allowed | The name of the target, location, and version are printed |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

### The madness of various commands
Here are examples of the different ways executables can present their version.
```
$ java --version
openjdk 11.0.8 2020-07-14
OpenJDK Runtime Environment (build 11.0.8+10-post-Ubuntu-0ubuntu118.04.1)
OpenJDK 64-Bit Server VM (build 11.0.8+10-post-Ubuntu-0ubuntu118.04.1, mixed mode, sharing)
$
```

```
$ bash --version
GNU bash, version 4.4.20(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
$
```

```
$ ansible --version
ansible 2.5.1
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/mrbruno/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.17 (default, Jul 20 2020, 15:37:01) [GCC 7.5.0]
$
```

```
$ python --version
Python 2.7.17
$
```

```
$ docker --version
Docker version 17.09.0-ce, build afdb6d4
$
```

### Simple use of the tool 
```
$ versions java bash ansible python docker
Name     Location  Version
java     /usr/bin  11.0.8
bash     /bin      4.4.20(1)-release
ansible  /usr/bin  2.5.1
python   /usr/bin  2.7.17
docker   /usr/bin  17.09.0-ce
$
```

Note that annoying trailing characters are removed from the "version token" such as the comma from `docker`. 

### Using `--dumb` option
```
$ versions --dumb java bash ansible python
Name     Location  Version
java     /usr/bin  openjdk 11.0.8 2020-07-14 OpenJDK Runtime Environment (build 11.0.8+10-post-Ubuntu-0ubuntu118.04.1) OpenJDK 64-Bit Server VM (build 11.0.8+10-post-Ubuntu-0ubuntu118.04.1, mixed mode, sharing)
bash     /bin      GNU bash, version 4.4.20(1)-release (x86_64-pc-linux-gnu) Copyright (C) 2016 Free Software Foundation, Inc. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>  This is free software; you are free to change and redistribute it. There is NO WARRANTY, to the extent permitted by law.
ansible  /usr/bin  ansible 2.5.1   config file = /etc/ansible/ansible.cfg   configured module search path = [u'/home/mrbruno/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']   ansible python module location = /usr/lib/python2.7/dist-packages/ansible   executable location = /usr/bin/ansible   python version = 2.7.17 (default, Jul 20 2020, 15:37:01) [GCC 7.5.0]
python   /usr/bin  Python 2.7.17
$
```

### Using `--version` option
```
$ versions --version java
11.0.8
$ 
```

### `git`-based example
I honestly don't use the tool much on my own tools but maybe I should!  I haven't provided a `--version` option for any of my tools and I don't really want to have to maintain a version level either.  But I figured I could mine the information from `git`:
```
$ versions versions
Name      Location           Version
versions  /home/mrbruno/bin  2020.07.06-124824 77fb213 jpfuntne@cisco.com Correcting test for --version
$
```

The version is made up of the output from `git log -1 executable`:
1. The date and time of the last change: `YYYY.mm.dd-HHMMSS`
2. The short SHA1 of the commit
3. The user who made the change - that's my work email at the time I made the change
4. The remainder is the first line of the comment from the commit

### Relative & absolute paths
If you use a slash in a target name, it is taken as a relative or absolute path and the tool will not search `$PATH`:

```
$ versions bin/versions
Name      Location           Version
versions  /home/mrbruno/bin  2020.07.06-124824 77fb213 jpfuntne@cisco.com Correcting test for --version
$
```

## Notes

- The tool gets the version from:
  1. Output from `executable --version`
  2. Output from `executable -version` - I can't recall an example of an executable that works this way but it is supported
  3. An attempt is made to generate information from `git` if the executable is part of a repository.  I did that mostly for my tools but honestly don't use it very much (see above example)   
- See also the [`pythons`](pythons.md) tool
