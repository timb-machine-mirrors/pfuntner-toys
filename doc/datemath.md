# `datemath`

## Purpose
Perform arithmetic on a date or two dates:

  - Calculate the difference between two dates
  - Add or subtract a `timedelta` from a date

## Syntax
```
Syntax:
        datemath date1 - date2
        datemath date1 +/- timedelta

Where:
  date1 and date2 can be expressed as:
     "now"		ex: now
     %Y/%m/%d		ex: 2018/04/03
     %Y/%m/%dT%H:%M	ex: 2018/04/03T12:00
     %Y/%m/%dT%H:%M:%S	ex: 2018/04/03T12:00:00
     %H:%M:%S		ex: 12:00:00
     %H:%M		ex: 12:00
  timedelta can be expressed as:
     [INTd][INTh][INTm][INTs] ex: 1d12h
```

## Example

```
```

## Notes

  - When doing math between two dates, you need not worry about which date is earlier than the other.  The script tells you the amount of time between the dates.
