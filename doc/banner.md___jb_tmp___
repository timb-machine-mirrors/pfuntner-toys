# `banner`

## Purpose
Prints a message in a banner.  I often use this inside scripts or in interactive loop as an eye catcher.

## Syntax
```
Syntax: banner [--character C] [--box] [--left] [--center] [--middle] [--right] [--color COLOR] [text ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `--character C`  | Use `C` as the border character | The default is to use use a _box-style_ border.  See `--box`. |
|  `--box`  | Toggles use of the _box-style_ border: corner characters, vertical bars on the sides, and horizontal bars on the top and bottom. If box-style borders are disabled and an alternate character is not specified, a _hash_ character is used instead. | The default is to use use a _box-style_ border.  |
|  `--left`  | Text is left-justified, assuming there are multiple lines of text. | This is the default |
|  `--center`  | Text is centered, assuming there are multiple lines of text. | The default is to left-justified text |
|  `--right`  | Text is right-justified, assuming there are multiple lines of text. | The default is to left-justified text |
| `--color COLOR` | Print the banner in a specific color.  This must be one of: `black`, `blue`, `brown`, `cyan`, `darkgray`, `green`, `lightblue`, `lightcyan`, `lightgray`, `lightgreen`, `lightpurple`, `lightred`, `orange`, `purple`, `red`, `white`, or `yellow` but best effors are taken  to normalize input (eg: `Light Red`) and accept unambiguous abbreviations (eg: `blu`). | The default is the default foreground color for the terminal.  This is typically customizable by your emulator/terminal so to definitively say the _default_ is black or white is inaccurate. |

- Text is taken from the command line after any options and arguments, if there is such text.
- Text is taken from stdin if there is no text after the options and arguments, assuming stdin is directed via a file or pipe.  The command fails if there are no arguments and stdin is the terminal.

## Examples

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

### Color

![Example of banner with --color option](https://raw.githubusercontent.com/pfuntner/toys/master/images/banner-color-example.png)
