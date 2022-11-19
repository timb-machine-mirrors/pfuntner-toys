# `timestamp-my-file`

## Purpose
Adds a timestamp to one or more files by appending `_YYYY-mm-dd_HH.MM.SS.ffffff` to the name(s).

## Syntax
```
Syntax: timestamp-my-file file ...
```

### Arguments
Specify one or more files.

## Example

```
$ touch foo
$ timestamp-my-file foo
renamed 'foo' -> 'foo_2022-03-13_15.47.55.525369'
$ timestamp-my-file foo_2022-03-13_15.47.55.525369
2022-03-13 15:48:10,319 WARNING /home/mrbruno/bin/timestamp-my-file:56 foo_2022-03-13_15.47.55.525369 appears to already have timestamp
$
```

## Notes

- My use case that drove me to create the script is I was going to run a command that I know will write to a file or directory and I wanted to save an old copy of the file/directory.
- The script uses `mv -v` under the covers to do the renames.
- `mv` will print any errors:
    - file does not exist
    - no permission to move the file
    - etc.
