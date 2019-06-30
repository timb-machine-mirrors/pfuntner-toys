# `br`

## Purpose
`br` stands for _browse_.  This is a script that you kind of have to use to appreciate. It reads from stdin, stashes the data verbatim in a temporary file, launches vi on the file, and then removes the file when you're done. So it's a little bit like `more`/`less` but I think it's much more flexible and you have a full editor to play with.  I think this was inspired by my time on Windoze when I had a script to launch notepad.exe on data coming from stdin.  That was nice but had some issues and I like this better.

Alternatively, if you run it without redirecting stdin and give it one or more filenames, it launches `vi` in read-only mode. I used to have an alias for years that would only do read-only editing but I finally combined them together and the script has proven very useful.  I often appreciate an extra safeguard to help keep me from changing a file by accident.

## Syntax
```
Syntax: br [-g] [-n] [ [ OPTS ] FILENAME ... ]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-g` `--gvim` | Use {gvim} instead of `vi`/`vim` | Available only on Windoze |
| `-n` {--notepad} | Use Windoze {notepad} of `vi`/`vim` | Available only on Windoze |

- If you supply one or more filenames, it invokes `vi` on the files in read-only mode.
- If you don't supply any filenames, the script copies all the data from stdin into a temporary file and launches `vi` on that file.

## Example
The script is too interactive to give a good example. Just try it out.

## Notes

- It is expected that you haven't redirected stdout.  The script prints and error message and exits if this is not the case.
- The Python [`tempfile.mkstemp()`](https://docs.python.org/2/library/tempfile.html) method is used to arrive at the temporary file name.
- Signal handlers are set up to try to handle situations when the user used ctrl-C while the script is running to ensure the temporary file is removed.
- I've definitely seen problems using `br` from Git bash on Windoze but I can't even start an interactive Python session from Git bash so I don't feel too bad.  So I don't know how to fix this yet but maybe someday!  I've basically given up trying to use the command on Git bash for now because it just falls flat on its face.  I've gone back to `alias br='vi -R'` in Git bash because that's usually what I want to do.
- I spent a bit of time trying to get this working on Windoze as well as Unix.  I usually use cygwin for my shell on Windoze *(which has its own pecularities with respect to paths outside of the cygwin domain, especially when `notepad` is used)* but I think I also tested it from a regular Windoze command prompt.
- You can specify options for `vi` such as a command to execute before giving you control.  For example, to have it not wrap the lines, you could use:

  ```
  br -- -c'set nowrap' filename
  ```
  
  Notes:
  - The `--` is very important - this tells `br` that its options are complete so the `-c` will be passed to `vi`
  - The lack of a space after `-c` is also significant.  If you pass and operand to an option, you cannot leave any space or else `br` will think it's a filename and try to fully-qualify it
