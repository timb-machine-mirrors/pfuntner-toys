# `flow`

## Purpose
Join stdin into columns in `ls`-style

## Syntax
```
Syntax: flow [-w num|--width=num] [-v|--vertical] [-h|--horizontal] [--sep CHAR]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-w` or `--width` | Defines the width of the window | By default the tool will sense the width of the window automatically but this option can override that |
| `-v` or `--vertical` | Use vertical style - The first line is the first element of the first row, the second element is the first element of the second row, etc. | By default, horizontal style is used |
| `-h` or `--horizontal` | Use horizontal style - The first line is the first element of the first row, the second element is the second element of the first row (if it fits), etc. | By default, horizontal style is used |
| `--sep CHAR` | Define separator chracter | The default separation chracter is a space |

## Example

```
$ peval '"\n".join([str(num) for num in range(25)])' | flow  -w 20
0  1  2  3  4  5
6  7  8  9  10 11
12 13 14 15 16 17
18 19 20 21 22 23
24
$ peval '"\n".join([str(num) for num in range(25)])' | flow  -w 20 --sep \|
0 |1 |2 |3 |4 |5
6 |7 |8 |9 |10|11
12|13|14|15|16|17
18|19|20|21|22|23
24|  |  |  |  |
$ peval '"\n".join([str(num) for num in range(25)])' | flow -v  -w 40 --sep \|
0 |2 |4 |6 |8 |10|12|14|16|18|20|22|24
1 |3 |5 |7 |9 |11|13|15|17|19|21|23|
$
```

## Notes

- Inspired by default output of a simple `ls` command
