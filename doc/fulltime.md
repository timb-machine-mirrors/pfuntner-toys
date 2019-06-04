# `fulletime`

## Purpose
Invoke command using all options of `time` utility.

I've used the `time` utility for years but until recently didn't realized there was a plethora of options available for all sorts of information about the command: memory, context-switching, etc.  I had no idea!!  Various implementations of `time` on different platforms had varied options so I came up with this script that:

  1. scrapes the options and descriptions from `time` help output
  1. invokes the command using all the options discovered from the first step

## Syntax
```
Syntax: fulltime [-h] [-v] cmd [arg [arg ...]]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

```
$ fulltime sudo find / | headtail
       1 /
       2 /dev
       3 /dev/loop11
       4 /dev/v4l
       5 /dev/v4l/by-path
find: ‘/run/user/1000/gvfs’: Permission denied
Command exited with non-zero status 1

  sudo find /: Name and command line arguments of the command being timed.
  0: Average size of the process's unshared data area, in Kilobytes.
  0:14.55: Elapsed real (wall clock) time used by the process, in [hours:]minutes:seconds.
  0: Number of major, or I/O-requiring, page faults that occurred while the process was running. These are faults where the page has actually migrated out of primary memory.
  614864: Number of file system inputs by the process.
  0: Average total (data+stack+text) memory use of the process, in Kilobytes.
  10404: Maximum resident set size of the process during its lifetime, in Kilobytes.
  0: Number of file system outputs by the process.
  37%: Percentage of the CPU that this job got. This is just user + system times divided by the total running time. It also prints a percentage sign.
  3093: Number of minor, or recoverable, page faults. These are pages that are not valid (so they fault) but which have not yet been claimed by other virtual pages. Thus the data in the page is still valid but the system tables must be updated.
  3.57: Total number of CPU-seconds used by the system on behalf of the process (in kernel mode), in seconds.
  1.93: Total number of CPU-seconds that the process used directly (in user mode), in seconds.
  0: Number of times the process was swapped out of main memory.
  0: Average amount of shared text in the process, in Kilobytes.
  4096: System's page size, in bytes. This is a per-system constant, but varies between systems.
  322: Number of times the process was context-switched involuntarily (because the time slice expired).
  14.55: Elapsed real (wall clock) time used by the process, in seconds.
  0: Number of signals delivered to the process.
  0: Average unshared stack size of the process, in Kilobytes.
  0: Number of socket messages received by the process.
  0: Number of socket messages sent by the process.
  0: Average resident set size of the process, in Kilobytes.
  75795: Number of times that the program was context-switched voluntarily, for instance while waiting for an I/O operation to complete.
  1: Exit status of the command.
         .
         .
         .
 1647050 /root/.rpmdb/.dbenv.lock
 1647051 /root/.rpmdb/.rpm.lock
 1647052 /root/.rpmdb/Requirename
 1647053 /root/.rpmdb/Packages
 1647054 /root/.rpmdb/__db.003
$
```

## Notes

- The output from `time` goes to stderr
- If your command has options, you might have to precede the command with `--` to instruct the shell to not apply the options to `fulltime` - the options are part of arguments for the command that `fulltime` executes.
