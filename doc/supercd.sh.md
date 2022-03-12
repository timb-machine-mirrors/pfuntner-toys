# `supercd.sh`

## Purpose
I use this tool as a replacement (or frontend) to `cd`.  It will seek my home directory for a single directory that matches the input regular expression and changes my current working directory to that directory.

## Syntax
```
Syntax: supercd.sh [-verbose] pattern
```

### Options and arguments
| Option                  | Description              | Default                                   |
|-------------------------|--------------------------|-------------------------------------------|
| `-v`                    | Enable verbose debugging | Debugging is not enabled                  |

## Examples

### Working example
```
$ # This demonstrates what happens if your don't source the tool
$ supercd.sh foobar
Note: /home/mrbruno/bin/supercd.sh is not sourced
$ # The target does not exist
$ supercd foobar
No matches for foobar
$ # Create the target
$ mkdir ~/foobar
$ # Identify original directory
$ pwd
/home/mrbruno/repos/toys/tmp/20220312091536736347380
$ # Change to destination
$ supercd foobar
/home/mrbruno/foobar
$ # Prove we have changed to the directory
$ pwd
/home/mrbruno/foobar
$ 
```

### Tool is not sourced
```
$ supercd.sh foobar
Note: /home/mrbruno/bin/supercd.sh is not sourced
$ 
```

### No directories match target pattern
```
$ supercd foobar
No matches for foobar
$ 
```

### Too many directories match target pattern & refining pattern
```
$ mkdir ~/foobar ~/foobar-foo
$ supercd foobar
Too many matches for foobar
  /home/mrbruno/foobar-foo
  /home/mrbruno/foobar
$ supercd foobar\$
/home/mrbruno/foobar
$ 
```

### Verbose output
The tool makes use of a Python script to look at the user's home directory and locate directories that match the pattern.  The Python script will not show errors by default but they can be displayed by using the debugging option:
```
$ supercd -v foobar
2022-03-12 10:11:19,166 INFO /home/mrbruno/bin/supercd.py:22 listdir('/home/mrbruno/extra/lost+found') error: PermissionError(13, 'Permission denied')
Too many matches for -v foobar
  /home/mrbruno/foobar-foo
  /home/mrbruno/foobar
$ 
```

## Notes

- The tool is designed to be used interactively from a login shell.  The tool must be _sourced_ because it changes the current working directory.  I purposefully called the script `sueprcd.sh` so I could set up an alias to do the sourcing automatically so I don't have to think about it:
    ```
    alias supercd='. supercd.sh'
    ```
  You might wish to add such an alias to your `$HOME/.bashrc`.
- I'm lazy I often use this tool to jump into a directory without typing the entire name and without having to specify exactly where it is.  For example, I have worked on a team where we made changes to a few dozen different Git repos.  I was able to navigate to the easily by using unique targets to the repos without having to type the entire path. 
