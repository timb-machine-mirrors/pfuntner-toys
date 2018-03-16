# `br`

## Purpose
`br` stands for _browse_.  This is a script that you kind of have to use to appreciate. It reads from stdin, stashes the data verbatim in a temporary file, launches vi on the file, and then removes the file when you're done. So it's a little bit like more but I think it's much more flexible and you have a full editor to play with. 

Alternatively, if you run it without redirecting stdin and give it one or more filenames, it launches `vi` in read-only mode. I used to have an alias for years that would only do read-only editing but I finally combined them together and the script has proven very useful.  I'm still getting used to using it as a filter for stdin, using `less` instead.  `less` is nice but it's not a full `vi`!

## Syntax
```
Syntax: br [FILENAME ... ]
```

### Options and arguments
There are no options.

- If you supply one or more filenames, it invokes `vi` on the files in read-only mode.
- If you don't supply any filenames, the script copies all the data from stdin into a temporary file and launches `vi` on that file.

## Example
The script is too interactive to give a good example. Just try it out.

## Notes

- It is expected that you haven't redirected stdout.  The script prints and error message and exits if this is not the case.
- The Python [`tempfile.mkstemp()`](https://docs.python.org/2/library/tempfile.html) method is used to arrive at the temporary file name.
- Signal handlers are set up to try to handle situations when the user used ctrl-C while the script is running to ensure the temporary file is removed.
- I've definitely seen problems using `br` from Git bash on Windows but I can't even start an interactive Python session from Git bash so I don't feel too bad.  So I don't know how to fix this yet but maybe someday!  I've basically given up trying to use the command on Git bash for now because it just falls flat on its face.  I've gone back to `alias vi='vi -R'` in Git bash because it's usually what I want to do.
