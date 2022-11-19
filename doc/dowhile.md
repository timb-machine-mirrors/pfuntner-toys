# `dowhile`

## Purpose
Runs a command _while_ its output contains (or doesn't contain) a specified string.

## Syntax
```
Syntax: dowhile [--negate|-v] [--ignorerc] string cmd ...
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v` or `--negate`  | Toggles whether the script will require the string is in the output or the string is not in the output. | The default is to run the command while the string is in the output. |
|  `--ignorerc` | Toggles whether the script will stop when the command exits with a non-zero status | The default is to exit if the command exit status is non-zero, regardless of the output. |

## Example

```
$ dowhile 10:33 date
2017-11-07 10:33:00.1510068780
Tue Nov  7 10:33:00 EST 2017

2017-11-07 10:33:15.1510068795
Tue Nov  7 10:33:15 EST 2017

2017-11-07 10:33:30.1510068810
Tue Nov  7 10:33:30 EST 2017

2017-11-07 10:33:45.1510068825
Tue Nov  7 10:33:45 EST 2017

2017-11-07 10:34:00.1510068840
Tue Nov  7 10:34:00 EST 2017

$
```

## Notes

- There are 15 seconds between each iteration
- Each iteration is preceded by the current timestamp
- Simple string comparison is done.  The string argument is **not** a regular expression.  I might improve it if I have a need to do so
- You may need to wrap the command around `bash -c "..."` in order to run complicated commands or have the shell interpret a `#!` line:
  ```
  dowhile jan bash -c 'date | tr "[A-Z]" "[a-z]"'
  ```
- You may wish to search for the empty string (`''`) if you don't care what the output contains - unless `-ignorerc` is used, the command will run until it exits with a non-zero status
