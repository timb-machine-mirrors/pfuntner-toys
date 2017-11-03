# `beeper`

## Purpose
This is a script that simply beeps forever - or at least until you kill it. The way I use it is I combine it with another command that I expect to run for several seconds, it not several minutes. beeper will let me know when the other command finishes.

## Syntax
```
Syntax: beeper
```

### Options and arguments
There are no options or arguments

## Example

```bash
$ date; sleep 5; date; beeper
Mon Aug 14 12:31:36 EDT 2017
Mon Aug 14 12:31:41 EDT 2017
***********************************************
* 2017-08-14 12:31:41.396286: Beeping started *
***********************************************
^C
*********************************************
* 2017-08-14 12:31:46.812411: Beeping ended *
*********************************************
$ 
```

## Notes

- In the example, `^C` stands for me entering ctrl-C to kill the script... otherwise it keeps running and beeping.
