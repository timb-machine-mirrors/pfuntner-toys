# `jsoncompare`

## Purpose
Compare two JSON or YAML files.  Any combination of styles is allowed

## Syntax
```
jsoncompare [-h] [-y] [--y1] [--y2] [--char-by-char] [--side-by-side] [-v] file1 file2
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-y` or `--yaml` | Treat both files as YAML | Both files are treated as JSON |
| `--y1` or `--yaml1` | Treat first file as YAML | The first file is treated as JSON |
| `--y2` or `--yaml2` | Treat second file as YAML | The second file is treated as JSON |
| `--char-by-char` | Compare strings character by character | Strings are compared in default compact `diff` style |
| `--side-by-side` | Compare strings side by side | Strings are compared in default compact `diff` style |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

```
$ head one.json two.yaml
==> one.json <==
[
  1,
  2,
  {
    "foo": "We'd sing, sing, sing\nI'm a lumberjack and I'm ok\nI sleep all night and I work all day"
  },
  5
]

==> two.yaml <==
- 1
- 3
- foo: 'We''d sing, sing, sing

    I''m a lumberjack & I''m ok

    I sleep all night and I work all day'
  bar: "2"
- 5

$ jsoncompare one.json two.yaml
/1: 2 vs 3  # <== element #1 (remember, lists start at element #0!) is the number 2 in the first file, 3 in the second file
/2: 1-element dict vs 2-element dict  # <== the inner list is a different size
/2/foo:  # <== There are differences in one line of the the group of three lines
2c2
< I'm a lumberjack and I'm ok
---
> I'm a lumberjack & I'm ok
$ jsoncompare --side-by-side one.json two.yaml
/1: 2 vs 3
/2: 1-element dict vs 2-element dict
/2/foo:  # <== --side-by-side shows the change in context
We'd sing, sing, sing                                           We'd sing, sing, sing
I'm a lumberjack and I'm ok                                   | I'm a lumberjack & I'm ok
I sleep all night and I work all day                            I sleep all night and I work all day
$ jsoncompare --char-by-char one.json two.yaml
/1: 2 vs 3
/2: 1-element dict vs 2-element dict
/2/foo:  # <== --char-by-char shows each character that differs
41,43c41
< a
< n
< d
---
> &
$
```

## Notes

- The `diff` utility is used to compare strings.  When the `--side-by-side` option is used, the option is passed to `diff`.
- If either file ends in `.yaml`, it is automatically treated as a YAML file, regardless of the options used
- You could combine `--side-by-side` and `--char-by-char` but it could produce a lot of output
