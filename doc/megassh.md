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
$ megassh vm-ubuntu-1,vm-ubuntu-2 hostname
vm-ubuntu-1: vm-ubuntu

vm-ubuntu-2: ubuntu20-vm2

$ 
```
### JSON output
Sometimes the default output can be rather confusing.  JSON can be a better altnerative and the output is machine readable.
```
$ megassh -j vm-ubuntu-1,vm-ubuntu-2 ls / \| head
{
  "vm-ubuntu-1": {
    "elapsed": "0:00:00.306379",
    "rc": 0,
    "start": "2022-12-24T08:33:53.691991",
    "stderr": [],
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
    "stop": "2022-12-24T08:33:53.998370"
  },
  "vm-ubuntu-2": {
    "elapsed": "0:00:00.305622",
    "rc": 0,
    "start": "2022-12-24T08:33:53.692859",
    "stderr": [],
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
    "stop": "2022-12-24T08:33:53.998481"
  }
}
$ 
```

I escaped the pipe symbol to have it run `wc` in the target system - I didn't want to do a _word count_ on the output of `megassh` itself! 

### Becoming root
Sure, you could use `sudo` but sometimes just slipping in `-b` (which I borrowed from Ansible) is easier.  Plus, if the command is made up of multiple commands, everything is run as root!
```
$ megassh -b vm-ubuntu-1,vm-ubuntu-2 -- find / -type f \| wc
vm-ubuntu-1:  475313  475738 30827549
vm-ubuntu-1: find: ‘/run/user/1000/gvfs’: Permission denied

vm-ubuntu-2:  437455  437878 28006833
vm-ubuntu-2: find: ‘/run/user/1000/gvfs’: Permission denied

$ megassh -b vm-ubuntu-1,vm-ubuntu-2 -- ls -ld /run/user/1000/gvfs
vm-ubuntu-1: ls: cannot access '/run/user/1000/gvfs': Permission denied

vm-ubuntu-2: ls: cannot access '/run/user/1000/gvfs': Permission denied

$ megassh -b vm-ubuntu-1,vm-ubuntu-2 -- ls -ld /run/user/1000/
vm-ubuntu-1: drwx------ 12 mrbruno mrbruno 360 Dec 23 17:50 /run/user/1000/

vm-ubuntu-2: drwx------ 12 mrbruno mrbruno 380 Dec 23 17:39 /run/user/1000/

$ 
```
I'm not sure what's going on with `/run/user/1000` but it's clearly something even root doesn't have access to.

### Encoding the command
Consider that when you `ssh` to a target, you are usually an unprivileged user and you have to think about in what contexts portions of your command are run.  You might try to escape metacharacters but you likely have to escape _**those**_ escapes and it's just a big headache that makes you wish you were a manager ☺.

What the `--encode` option does is that it encodes the entire command with `base64` on the sending side before it ever sees the target system.  It doesn't get decoded until the command is actually ready to be executed where the output of `base64 -d` is fed directly into a shell.

`--encode` is especially powerful when combined with `--become` because the whole smash runs as root!

An example might help explain this better but this is one of my favorite options.
```
$ megassh -eb all -- 'find /etc/ssh* -name \*sshd\* -type f | xargs -i sudo grep -Pv "^\s*(#.*)?\$" /dev/null {}'
vm-ubuntu-1: /etc/ssh/sshd_config:Include /etc/ssh/sshd_config.d/*.conf
vm-ubuntu-1: /etc/ssh/sshd_config:Port 222
vm-ubuntu-1: /etc/ssh/sshd_config:ChallengeResponseAuthentication no
vm-ubuntu-1: /etc/ssh/sshd_config:UsePAM yes
vm-ubuntu-1: /etc/ssh/sshd_config:X11Forwarding yes
vm-ubuntu-1: /etc/ssh/sshd_config:PrintMotd no
vm-ubuntu-1: /etc/ssh/sshd_config:AcceptEnv LANG LC_*
vm-ubuntu-1: /etc/ssh/sshd_config:Subsystem	sftp	/usr/lib/openssh/sftp-server

vm-ubuntu-2: /etc/ssh/sshd_config:Include /etc/ssh/sshd_config.d/*.conf
vm-ubuntu-2: /etc/ssh/sshd_config:ChallengeResponseAuthentication no
vm-ubuntu-2: /etc/ssh/sshd_config:UsePAM yes
vm-ubuntu-2: /etc/ssh/sshd_config:X11Forwarding yes
vm-ubuntu-2: /etc/ssh/sshd_config:PrintMotd no
vm-ubuntu-2: /etc/ssh/sshd_config:AcceptEnv LANG LC_*
vm-ubuntu-2: /etc/ssh/sshd_config:Subsystem	sftp	/usr/lib/openssh/sftp-server

$
```
Quite a command, huh?  Some notes:
- Both the `find` and `grep` commands are running as root
- I'm using `xargs -i` because I knew `find` would only discover one file and `grep` won't include the name of the file if it's only processing a single file.  I wanted the `grep` command to include `/dev/null` (which would never match) but `xargs` can only run one `grep` at a time.
- I escaped the dollarsign because it's a metacharacter and by the time it's run by the root shell on the target, it will be vulnerable to interpretation since it's only inside double quotes.

### Producing a tar file remotely, expanding it locally
Recently before writing up this doc, I had a use case where I wanted to duplicate a complex file tree from a remote system on my laptop.  I could use `scp` but that was pretty slow.  I came up with an alternative:

1. I used `megassh` to produce a compressed tarball on the remote system and encode it for transport back to my laptop
2. I added a pipeline to read the output from `megassh` & `tar`, decode the tarball, and extract its contents.
```
$ megassh -bqe vm-ubuntu-1 -- 'tar -czf - /etc/ssh* | base64' | base64 -d | tar -tzf -
tar: Removing leading `/' from member names
etc/ssh/
etc/ssh/ssh_host_ecdsa_key
etc/ssh/ssh_config.d/
etc/ssh/ssh_host_ecdsa_key.pub
etc/ssh/ssh_host_rsa_key
etc/ssh/sshd_config.d/
etc/ssh/ssh_host_ed25519_key
etc/ssh/ssh_import_id
etc/ssh/moduli
etc/ssh/ssh_host_ed25519_key.pub
etc/ssh/ssh_host_rsa_key.pub
etc/ssh/ssh_config
etc/ssh/sshd_config
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
- I feel like I should apologize for the examples.  I wish I could have started some diverse remote systems but there are no cloud providers where I could create an instance for free.  So what I did was I created local virtual machines with VirtualBox set up so I could `ssh` into them.  I probably could have found more diverse systems than two Ubuntu 20 machines but I didn't.
