# `pythons`

## Purpose
Show versions of Python interpreter

## Syntax
```
Syntax: pythons [-h] [-a] [-d] [-v]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-a`, `--all` | Find all instances of executables in `$PATH` | Only the first instance of each executable is reported |
| `-d`, `--dumb` | Do not try to parse out version | Logic is used to intelligently figure out a version. Usually this is the first token of the output that matches the regular expression `\d\.`
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

### From my everyday Ubuntu workstation
```
$ pythons
Name     Location  Version
python   /usr/bin  2.7.17
python2  /usr/bin  2.7.17
python3  /usr/bin  3.6.9
$ pythons --dumb
Name     Location  Version
python   /usr/bin  Python 2.7.17
python2  /usr/bin  Python 2.7.17
python3  /usr/bin  Python 3.6.9
$ 
```

### From a basic Amazon Linux 1 AWS instance
I spun up an instance from fresh and it didn't even have Python 3 so I installed it since most of my tools use it.
```
$ pythons
Name     Location  Version
python   /usr/bin  2.7.18
python2  /usr/bin  2.6.9
python3  /usr/bin  3.4.10
$
```
It's curious that `/usr/bin/python` is not the same as either `/usr/bin/python2` or `/usr/bin/python3` but it is what it is!!!

### Inside virtualenv
I used `virtualenv` to set up an alternate Python:
```
$ virtualenv -p python3 venv
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /media/mrbruno/tmp/venv/bin/python3
Also creating executable in /media/mrbruno/tmp/venv/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
$ . venv/bin/activate
(venv) $ pythons
Name     Location                     Version
python   /media/mrbruno/tmp/venv/bin  3.6.9
python2  /usr/bin                     2.7.17
python3  /media/mrbruno/tmp/venv/bin  3.6.9
(venv) $ pythons --all
Name     Location                     Version
python   /media/mrbruno/tmp/venv/bin  3.6.9
python   /usr/bin                     2.7.17
python2  /usr/bin                     2.7.17
python3  /media/mrbruno/tmp/venv/bin  3.6.9
python3  /usr/bin                     3.6.9
(venv) $ 
```
This shows you that `virtualenv` is basically prepending the `venv` directory to my `$PATH` in order to override the existing Python executables.

## Notes

- The following command is executed for each executable:
  ```
  executable --version
  ```
- See also the [`versions`](versions.md) tool.