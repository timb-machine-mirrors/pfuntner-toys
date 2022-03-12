# `more-head`

## Purpose
Displays as much of a file as possible in the current number of lines on the screen.

## Syntax
```
Syntax: more-head
```

### Options and arguments
There are no options or arguments

## Example
Imagine a command that prints many lines:

    $ Data.py | json | headtail
           1 {
           2   "booleans": [
           3     false,
           4     false,
           5     false,
             .
             .
             .
         144     "f3094778-edbc-4b0c-9cba-e54f2110db77",
         145     "fb79a67c-61d4-4deb-9467-5c08e0998b3c",
         146     "ee11fa67-f37f-4fa3-996d-345057acb659"
         147   ]
         148 }
    $ 

You might want to view as much of the top of the output as possible without counting the number of lines on the screen.  This script will sense the number of lines on the screen and print one line less than the number of lines on the screen.  It does one less to allow for the command to remain on the screen:

![`more-head` example](images/more-head.png)

## Notes

- I'm not crazy about the name of the command but I think of it as a hybrid of the classic `more` and `head` commands.
- The script reads from stdin so you must redirect input to the script or use a pipeline.
- The script does not account for lines to wide for the screen (although you could combine it with [`fitwidth`](fitwidth.md)).
- The script does not account for a command line so long that it doesn't fit on one screen so the entire command may not be visible.
