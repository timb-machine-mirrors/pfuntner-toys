# `beeper`

## Purpose
This is a script that simply beeps forever - or at least until you kill it... or the system is rebooted, or the user is killed, or aliens invade, etc. The way I use it is I combine it with another command that I expect to run for several seconds, if not several minutes. beeper will let me know when the other command finishes.

## Syntax
```
Syntax: beeper
```

### Options and arguments
There are no options or arguments

## Example

```
$ date; sleep 5; date; beeper
Wed Apr 18 10:53:13 EDT 2018
Wed Apr 18 10:53:18 EDT 2018
***********************************************
* 2018-04-18 10:53:18.981124: Beeping started *
***********************************************

*************************************************************
* 2018-04-18 10:53:23.738956: Beeping ended, 0:00:04.757832 *
*************************************************************
$
```

## Notes

- In the example, `^C` stands for me entering ctrl-C to kill the script... otherwise it keeps running and beeping.
- The message indicating that beeping has ended includes the duration.  In the example above, 4.78 seconds.
