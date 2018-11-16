# `peval`

## Purpose
Evalulate a Python expression

## Syntax
```
Syntax: peval [-i|--import MODULE] expression ...
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-i` or `--import`  | Import a module | Since the bulk of the code is just a print statement of the arguments on the command line, this option can be used to import a Python module such as `os`, `path`, `re`, etc. |

## Example

```
$ peval --import datetime 'datetime.datetime.now().isoformat()', 'range(25)'
('2018-09-25T17:07:10.967965', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
$ 
```

## Notes

- A lot of times, I'll open an interactive Python window to try things out but if I just want to look at a simple expression, this can save time.
- I don't consider it the best example but in [issue 23](https://github.com/pfuntner/toys/issues/23) I used `peval` to describe undesriable behavior with another tool
