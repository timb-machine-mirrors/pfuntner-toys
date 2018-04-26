# `extensions`

## Purpose
Print <a href="https://www.wikiwand.com/en/Filename_extension">_extensions_</a> of file names.  For each file, a line is printed in the following form:

  ```
Original filename|extension
  ```

## Syntax
```
Syntax: extensions [FILE ...]
```

### Options and arguments
There are no options.  One or more file names must be specified as arguments.

## Example

```
$ find . -type f | extensions | headtail
       1 ./pinger-20180215.out.gz|gz
       2 ./pinger-20180325.out.gz|gz
       3 ./pinger-20180304.out.gz|gz
       4 ./pinger-20180302.out.gz|gz
       5 ./pingbeep|
         .
         .
         .
     269 ./pinger-20180109.out.gz|gz
     270 ./pinger-20180419.out|out
     271 ./pinger-20180130.out.gz|gz
     272 ./pinger-20180201.out.gz|gz
     273 ./pingplot|
$ 
```
Note that this example makes use of the [`headtail`](headtail.md) tool.

## Notes

- If there is more than one period in a file name, the extension is everything that occurs after the **last** period.
- If there are no periods in a file name, it is considered to have _no extension_ and the output line will have a null string for the extension for that file.
- Extensions are based on the <a href="https://www.wikiwand.com/en/Basename">_basename_</a> of a path.  If you have a path such as `foo.bar/FOOBAR`, the file name has no extension since the period appears in the parent directory of the file.
