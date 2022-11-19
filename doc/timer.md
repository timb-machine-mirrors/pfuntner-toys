# `timer`

## Purpose
Runs a timer for a specified duration.  A progress meter is shown with details of:
  - current time
  - elapsed time in seconds
  - remaining time in seconds

The output is presented at intervals on a single line.

## Syntax
```
Syntax: timer [-v|--verbose] INT # seconds
        timer [-v|--verbose] INTs # seconds
        timer [-v|--verbose] INTm # minutes
        timer [-v|--verbose] INTh # hours
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

Since the output appears on a single line this isn't exactly what you'll see but this is an idea of what the output looks like.

```
$ timer 10 # ten seconds
2019-02-16 08:48:12.325835 ☐☐☐☐☐☐☐☐☐☐   0.00% 0.00 10.00
2019-02-16 08:48:14.580168 ☒☒☐☐☐☐☐☐☐☐  22.54% 2.25 7.75
2019-02-16 08:48:16.834748 ☒☒☒☒☒☐☐☐☐☐  45.09% 4.51 5.49
2019-02-16 08:48:21.092859 ☒☒☒☒☒☒☒☒☒☐  87.67% 8.77 1.23
$
```

## Notes

- The output columns are:
  - First two columns: the current date and time
  - Third column: graphic progress meter
  - Fourth column: percentage of the total duration - this is a reflection of the progress meter but in numeric form instead of graphic
  - Fifth column: current elapsed time in seconds
  - Sixth column: current remaining time in seconds
- The script seems to be a little slow starting on some platforms.  I'm not exactly sure what's going on but it's only delayed a couple of seconds.  You should only notice it for very small durations such as five seconds.
