# `banner`

## Purpose
Prints a message in a banner.  I often use this inside scripts or in interactive loop as an eye catcher.

## Syntax
```
Syntax: banner [--character C] [--box] [--left] [--center] [--middle] [--right] [text ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `--character C`  | Use `C` as the border character | The default is to use use a _box-style_ border.  See `--box`. |
|  `--box`  | Toggles use of the _box-style_ border: corner characters, vertical bars on the sides, and horizontal bars on the top and bottom. If box-style borders are disabled and an alternate character is not specified, an _hash_ character is used instead. | The default is to use use a _box-style_ border.  |
|  `--left`  | Text is left-justified, assuming there are multiple lines of text. | This is the default |
|  `--center`  | Text is centered, assuming there are multiple lines of text. | The default is to left-justified text |
|  `--right`  | Text is right-justified, assuming there are multiple lines of text. | The default is to left-justified text |

- Text is taken from the command line after any options and arguments, if there is such text.
- Text is taken from stdin if there is no text after the options and arguments, assuming stdin is directed via a file or pipe.  The command fails if there are no arguments and stdin is the terminal.

## Example

```
$ banner hello
┏━━━━━━━┓
┃ hello ┃
┗━━━━━━━┛
$ echo -e "The time is\n$(date)" | banner --center --box
################################
#         The time is          #
# Wed Nov  1 16:55:59 EDT 2017 #
################################
$ 
```
