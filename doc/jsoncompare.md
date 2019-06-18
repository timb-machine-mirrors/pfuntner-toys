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
| `--char-by-char` | Compare strings character by character | Strings are compared as entire strings |
| `--side-by-side` | Compare strings side by side | Strings are compared in default compact `diff` style |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

```
$ template
This is a template.  Please fill in the details and rock on.
$ 
```

## Notes

- The `diff` utility is used to compare strings.  When the `--side-by-side` option is used, the option is passed to `diff`.
- If either file ends in `.yaml`, it is automatically treated as a YAML file, regardless of the options used
