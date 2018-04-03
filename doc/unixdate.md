# `unixdate`

## Purpose
Invoke `date` command using Unix format on Windoze

## Syntax
```
Syntax: unixdate [date options]
```

### Options and arguments
See options and arguments for `date` such this on this [man page](http://linuxcommand.org/lc3_man_pages/date1.html)

## Example

```
$ unixdate                       # simplest form of the command
Tue Apr  3 08:22:23 EDT 2018

$ unixdate -u                    # specify -u along with the format that will be added
Tue Apr  3 12:22:29 UTC 2018

$ unixdate +%Y%m%d%H%M%S         # specify a specific format
20180403082255

$ /usr/bin/date                  # you can still get the "normal Windoze output"
Tue, Apr  3, 2018  8:26:13 AM

$ alias date=unixdate            # override /usr/bin/date with an alias
$ date -R                        # alternate way of specifiying a format
Tue, 03 Apr 2018 08:54:08 -0400

$
```

## Notes

- This script was created specifically with Windoze shells in mind (Cygwin and Git bash) that print the date in style inconsistent with a regular Unix shell.  There's nothing that stops you from using this script on a real Unix system but there's no purpose because the `date` command works as you might expect.
- If you don't specify your own format string, the script will supply a format string to print the date and time in the style you would see on a Unix system.
- You might want to set up an alias to this script so that any time you type `date` in a Windoze shell, you'll run this script instead.  I would encourage you add such an alias from your `~/.bashrc` but it's up to you.
