# `megassh`

## Purpose
A tool that performs ssh to one or more target systems.  Key features:
- target multiple systems with the same command
- compose complex commands with less interference from the shell

## Syntax
```
Syntax: megassh [-h] [-t] [-e] [-b] [-q] [-j | -r] [-v] hosts cmd [arg [arg ...]]
```

### Options and arguments
| Option        | Description                                                                                                                              | Default                                                                                                |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| `-h` `--help` | Show online help                                                                                                                         | Online Help is not provided                                                                            |
|  `-t` `--tty`   | Force pseudo-terminal allocation. Honestly, I can't remember the last time I had to use this option and don't remember use cases for it! |  |
|  `-e` `--encode` | Use base64 encoding to protect command.  This is especially useful with `--become`                                                       | The command is not encoded                                                                             |
|  `-b` `--become` | Use sudo on remote system                                                                                                                | There is no escalation                                                                                 |
|  `-q` `--quiet` | Use ssh -q                                                                                                                               | Nastygrams might be seen                                                                               |
|  `-j` `--json` | Produce JSON output                                                                                                                      | Output is printed in a simple format                                                                   |
|  `-r` `--raw`  | Produce raw output. Honestly, I can't remember the last time I had to use this option and don't remember use cases for it! | Output is printed in a simple format                                                                   |
| `-v` `--verbose` | Enable verbose debugging                                                                                                                 | Debugging is not enabled    |

## Examples

### Multiple targets
It's easy to run a command across multiple systems.
```
$ template
This is a template.  Please fill in the details and rock on.
$
```
### JSON output
Sometimes the default output can be rather confusing.  JSON can be a better altnerative and the output is machine readable.
```
$ template
This is a template.  Please fill in the details and rock on.
$
```
### Becoming root
Sure, you could use `sudo` but sometimes just slipping in `-b` (which I borrowed from Ansible) is easier.  Plus, if the command is made up of multiple commands, everything is run as root!
```
$ template
This is a template.  Please fill in the details and rock on.
$
```
### Encoding the command
Consider that when you `ssh` to a target, you are usually an unprivileged user and you have to think about in what contexts portions of your command are run.  You might try to escape metacharacters but you likely have to escape _**those**_ escapes and it's just a big headache that makes you wish you were a manager.

What the `--encode` option does is that it encodes the entire command with `base64` on the sending side before it ever sees the target system.  It doesn't get decoded until the command is actually ready to be executed where the output of `base64 -d` is fed directly into a shell.

An example might help explain this better but this is one of my favorite options.
```
$ template
This is a template.  Please fill in the details and rock on.
$
```
### Producing a tar file remotely, expanding it locally
Recently before writing up this doc, I had a use case where I wanted to duplicate a complex file tree from a remote system on my laptop.  I could use `scp` but that was pretty slow.  I came up with an alternative:

1. I used `megassh` to produce the tarball on the remote system and encode it for transport back to my laptop
2. I added a pipeline to read the output from `megassh` & `tar`, decode the tarball, and extract its contents.
```
$ template
This is a template.  Please fill in the details and rock on.
$
```
Thinking back, I probably could have done this without `megassh` as long as escalation wasn't needed and I was careful to protect the metacharacters.  

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

    In fact, I think Ansible inspired me to come up with this tool but such adhoc commands can be kind of cryptic.  Ansible has its own way of marshalling actions on a remote machine so it avoids the problem with encoding commands.  I think it uses temporary custom Python scripts.