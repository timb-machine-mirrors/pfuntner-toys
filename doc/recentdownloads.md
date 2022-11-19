# `recentdownloads`

## Purpose
Find recently downloaded files.  The script makes use of the `find` Unix utility to find files that have been modified in a time frame.

## Syntax
```
Syntax: recentdownloads [-v] [FLOAT(s|m|h|d)?]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

The optional operand specifies the beginning of the time frame.
- The first part of the operand must be a positive floating point number.
- If no suffix is specified, the number is interpreted as _days_.
- If a suffix of `s` is used, the number is interpreted as _seconds_.
- If a suffix of `m` is used, the number is interpreted as _minutes_.
- If a suffix of `h` is used, the number is interpreted as _hours_.
- If a suffix of `d` is used, the number is interpreted as _days_.

## Example

```
$ recentdownloads                                           # nothing in the past 24 hours
$ recentdownloads 14                                        # let's try the last 2 weeks
/home/mrbruno/downloads/rhett & link - gmm in 90 seconds.mp4
/home/mrbruno/downloads/zoom_amd64.deb
/home/mrbruno/downloads/Photos-20190209T195208Z-001.zip
/home/mrbruno/downloads/slack-desktop-3.3.7-amd64.deb
$ touch -t 300001010000 ~/downloads/foobar                  # create a file in the future
$ recentdownloads                                           # the `future file` is found
/home/mrbruno/downloads/foobar
$
```

## Notes

- I used this on both Unix and Windoze:
  - On Unix, `${HOME}/downloads` is searched
  - On Windoze, `${USERPROFILE}/downloads` is searched
