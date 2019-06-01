# `fitwidth`

## Purpose
Basically, this script shortens long strings.

So many times I've had output that just flowed over so many physical lines on my screen (potentially filling up the entire window, maybe with a **single** line that's **extremely** long) that make the output virtually impossible to read.  This script simplifies the output, perhaps by making every line fit on the physical window.

## Syntax
```
Syntax: fitwidth [--width INT] [--beginning|--middle|--ending] [file ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `--width INT` | Specifies the maximum length of lines to print out | The default width is based on `tput cols` which reports the current width of the shell window. |
| `--beginning` | Remove characters from the beginning of the each line until it is no longer than the desired width | `--middle` is the default behavior | 
| `--middle` | Remove characters from the middle of the each line until it is no longer than the desired width | `--middle` is the default behavior | 
| `--ending` | Remove characters from the ending of the each line until it is no longer than the desired width | `--middle` is the default behavior | 

## Example

```
$ tput cols
170
$ peval "'1234567890'*25"
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
$ peval "'1234567890'*25" | fitwidth
1234567890123456789012345678901234567890123456789012345678901234567890123456789012 ... 89012345678901234567890123456789012345678901234567890123456789012345678901234567890
$ peval "'1234567890'*25" | fitwidth --ending
123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345 ....
$ peval "'1234567890'*25" | fitwidth --beginning
.... 678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
$ peval "'1234567890'*25" | fitwidth --width 10
12 ... 890
$ 
```

This example makes use of my [`peval`](peval.md) tool.

## Notes

- When data is removed from a line in order to meet the desired width, they are replaced by three periods surrounded by a blank on either side.

  When a line is short enough to fit the desired width, it is not changed when it is printed.
