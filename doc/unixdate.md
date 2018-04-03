# `unixdate`

## Purpose
Invoke `date` command using Unix format on Windoze

## Syntax
```
Syntax: unixdate [date options]
```

### Options and arguments
See options and arguments for `date` util such this [man page](http://linuxcommand.org/lc3_man_pages/date1.html)

## Example

```
$ unixdate
Tue Apr  3 08:22:23 EDT 2018

$ unixdate -u
Tue Apr  3 12:22:29 UTC 2018

$ unixdate +%Y%m%d%H%M%S
20180403082255

$ /usr/bin/date
Tue, Apr  3, 2018  8:26:13 AM

$
```

## Notes

- This script was created specifically with Windoze shells in mind (Cygwin and Git bash) that print the date in style inconsistent with a regular Unix shell.
- If you don't specify your own format string, the script will supply a format string to print the date and time in the style you would see on a Unix system.
- You might want to set up an alias to this script so that any time you type `date` in a Windoze shell, you'll run this script instead.
