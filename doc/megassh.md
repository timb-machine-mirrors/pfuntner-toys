# `megassh`

## Purpose
A tool that performs ssh to one or more target systems.  Key features:
- target multiple systems with the same command
- compose complex escalated commands without interference from the shell

## Syntax
```
Syntax: megassh [-h] [-b] [-j] [-v] hosts cmd [arg [arg ...]]
```

### Arguments
| Option | Description                                                                                                       |
|--------|-------------------------------------------------------------------------------------------------------------------|
| `hosts`  | A comma-separated list of hostnames.  This can be `all` and `megassh` gets the list of hosts from `~/.ssh/coonfig` |
| `cmd [arg [arg ...]]` | Any command arguments.  This can be in the form of a complicated pipeline or multiple commands separated by semicolons |

### Options
| Option        | Description                                                                                                                | Default                                                                                                |
|---------------|----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| `-h` `--help` | Show online help                                                                                                           | Online Help is not provided                                                                            |
|  `-b` `--become` | Use sudo to escalate to superuser on remote system                                                                      | There is no escalation                                                                                 |
|  `-j` `--json` | Produce JSON output                                                                                                        | Output is printed in a simple format                                                                   |
| `-v` `--verbose` | Enable verbose debugging                                                                                                   | Debugging is not enabled    |

## Examples

### Multiple targets
It's easy to run a command across multiple systems.
```
$ megassh vm1,vm2 hostname \; grep PRETTY_NAME /etc/os-release
Host: vm1
vm1
PRETTY_NAME="Ubuntu 22.04.3 LTS"

Host: vm2
vm2
PRETTY_NAME="AlmaLinux 9.3 (Shamrock Pampas Cat)"
$ 
```
### JSON output
Sometimes the default output can be rather confusing.  JSON can be a better alternative and the output is machine readable.
```
$ megassh -j all ls / \| head
[
  {
    "host": "vm1",
    "stdout": [
      "bin",
      "boot",
      "cdrom",
      "dev",
      "etc",
      "home",
      "lib",
      "lib32",
      "lib64",
      "libx32"
    ],
    "stderr": [],
    "rc": 0,
    "elapsed": "0:00:01.201967",
    "hostname": "localhost",
    "user": "mrbruno",
    "port": "3022"
  },
  {
    "host": "vm2",
    "stdout": [
      "afs",
      "bin",
      "boot",
      "dev",
      "etc",
      "home",
      "lib",
      "lib64",
      "media",
      "mnt"
    ],
    "stderr": [],
    "rc": 0,
    "elapsed": "0:00:00.801365",
    "hostname": "localhost",
    "user": "mrbruno",
    "port": "4022"
  }
]
$  
```

I escaped the pipe symbol to have it run `head` in the target system - I didn't want it run locally on the output of `megassh` itself!  `head` is run remotely as the last part of the pipeline. 

If your hosts are present in `~/.ssh/config`, all of the information **about** that host in the config file (such as user or port) is included.

### Becoming root
Escalation to superuser isn't especially difficult but the trick is to run everything in the context of the root user and prevent the initial shell interpret commands, variables, etc **before** escalation.  When you use the `-b` option, `megassh` will automatically perform base64 encoding while the command is in transit.  The encoding isn't decoded until after escalation!  This avoids the complication of escaping metacharacters - and potentially escaping the escapes!!  What a nightmare!

```commandline
$ megassh all 'echo $USER sees $(find / 2>/dev/null | wc -l) files'
Host: vm1
mrbruno sees 489411 files

Host: vm2
mrbruno sees 215062 files
$ megassh -b all 'echo $USER sees $(find / 2>/dev/null | wc -l) files'
Host: vm1
root sees 563058 files

Host: vm2
root sees 273445 files
$ 
```
Slick, eh?  All I had to do was slip in the `-b` option - I didn't touch the rest of the command!

## Notes

- You might use [ansible-hosts](ansible-hosts.md) to help construct the target portion of a command
 
    ```
    $ megassh ... $(ansible-hosts --comma all) ...
    ```
    The `--comma` option is key to concatenate the system names properly.
- The script works best when:
    - You've set up your `$HOME/.ssh/config` with particulars about your remote systems (users, keys, ports, etc) so you can just refer to them with their familiar name
    - You've enabled password-less `ssh` to the remote system
    - You've enabled password-less `sudo` on the remote system

    I've never used the script any other way and don't know how the password prompts would interfere.
- You could work up Ansible ad-hoc commands that might do similar things:
 
    ```
    $ ansible -m command -a hostname all
    ```

    In fact, I think Ansible inspired me to come up with this tool but such adhoc commands can be kind of awkward and cryptic and output is not as nice as `megassh`.  Ansible has its own way of marshalling actions on a remote machine so it avoids the problem with encoding commands.  I think it uses temporary custom Python scripts - `megassh` does not create temporary files (unless you do that in your command, of course!).
- My examples might look a little contrived.  I did them from home pointing to a couple of virtual machines running in VirtualBox on my home computer - that's why the ports look a little strange.  I think the ports are 22 in the VMs but I map them to something else in the host and _hide_ the port in the ssh config file so I don't have to remember the details.
