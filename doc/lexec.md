# `lexec`

## Purpose
Locate executables

## Syntax
### Unix
```
Syntax: lexec [--verbose] pattern ...
```
Note that the pattern is a Python-style regular expression, not bash:

- The regular expressions are not anchored unless you use the `^` or `$` metacharacters
- The asterisk metacharacter repeats the expression that precedes the asterisk
- etc.

### Windoze only
```
Syntax: lexec [--verbose] [-s] pattern ...
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-s` or `--system` | Windoze only option: Search in _system_ directories as well as non-system directories.  See the _note_ for a definition of system directories and explanation.  | Do not search in system directories |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example
Here's an example that uses my [flow](flow.md) tool on Linux:
```
[mrbruno@bruno-meerkat ~]$ lexec git | flow
/usr/bin/git-shell                 /usr/bin/sgitopnm                  /usr/bin/git-receive-pack          /usr/bin/git
/usr/bin/git-upload-archive        /usr/bin/git-upload-pack           /home/mrbruno/bin/git-log          /home/mrbruno/bin/gitpush.sh
/home/mrbruno/bin/gitstatus.py     /home/mrbruno/bin/old-git          /home/mrbruno/bin/gitrepos         /home/mrbruno/bin/gitstatus
/home/mrbruno/bin/git-files        /home/mrbruno/bin/git-pushed       /home/mrbruno/bin/isgit            /home/mrbruno/bin/gitdiffs
/home/mrbruno/bin/gitdiff          /home/mrbruno/bin/gitter           /home/mrbruno/bin/gitsubs          /home/mrbruno/bin/gityup.py
/home/mrbruno/bin/git-stale        /home/mrbruno/bin/git-diff         /home/mrbruno/bin/git-pulls        /home/mrbruno/bin/gitbranches.py
/home/mrbruno/bin/gitpulls.sh      /home/mrbruno/bin/git-recent-files /home/mrbruno/bin/git-branches     /home/mrbruno/bin/gitdiff.py
/home/mrbruno/bin/whatgit          /home/mrbruno/bin/git-new-files    /home/mrbruno/bin/gitloggrep       /home/mrbruno/bin/gitpush.py
/home/mrbruno/bin/git-commit-check /home/mrbruno/bin/git-clone        /home/mrbruno/bin/git-extract      /home/mrbruno/bin/git-push
/home/mrbruno/bin/git-cat
[mrbruno@bruno-meerkat ~]$
```

Yes, I have a lot of files with "git" in the name and not all of them are even in this repo.  I might not even use some of them anymore.  I'm a packrat!

## Notes

- The tool looks for executable files in directories that make up the shell's `$PATH` environment variable
- No, _Windoze_ is **not** a misspelling.  It is the way I spell the operating system and if you don't like it, tough.
- Windoze system directories are:
    - `/c/Windows`
    - `/c/Program Files`

  I found when using the tool on Cygwin and not ignoring these directories took an extraordinary amount of time and I was rarely interested in those files anyway.  So by default they are ignored.
