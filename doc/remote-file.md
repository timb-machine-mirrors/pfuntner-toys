# `remote-file`

## Purpose
Read or write a remote file as a filter

## Syntax
```
Syntax: remote-file [-h] [-b] [-q] [-v] target
```
### Positional arguments
| Argument | Description                                                                                        | Default |
|----------|----------------------------------------------------------------------------------------------------|---------|
| `target` | The target system and file: `system:path`.  Examples: `foo:/absolute/path`, `foo@bar:relative/path` | None    |


### Options
| Option           | Description                                                             | Default                        |
|------------------|-------------------------------------------------------------------------|--------------------------------|
| `-b`, `--become` | Use `sudo` to escalate to root on remote system before reading/writing. | The initial `ssh` user is used |
| `-q`, `--quiet`  | Use the `ssh -q` option                                                 | Extra output might appear      |
| `-v`             | Enable verbose debugging                                                | Debugging is not enabled       |

## Examples

### Reading from a remote file
```
$ remote-file vm1:/etc/os-release | tr = \\n | tr -d \" | table.py -i form -o json | jq .[0]
{
  "PRETTY_NAME": "Ubuntu 22.04.3 LTS",
  "NAME": "Ubuntu",
  "VERSION_ID": "22.04",
  "VERSION": "22.04.3 LTS (Jammy Jellyfish)",
  "VERSION_CODENAME": "jammy",
  "ID": "ubuntu",
  "ID_LIKE": "debian",
  "HOME_URL": "https://www.ubuntu.com/",
  "SUPPORT_URL": "https://help.ubuntu.com/",
  "BUG_REPORT_URL": "https://bugs.launchpad.net/ubuntu/",
  "PRIVACY_POLICY_URL": "https://www.ubuntu.com/legal/terms-and-policies/privacy-policy",
  "UBUNTU_CODENAME": "jammy"
}
$ 
```
 [`table.py`](table.md) is an alias to another one of my tools.  It also uses [`jq`](https://jqlang.github.io/jq/) which is a popular third-party useful command.
 
I know the command is complicated but I like the result.  This is **not** the first version of the command and I had to work at it a little to get it to do exactly what I want.  I was lucky that a comma wasn't used anywhere in the values.  If would be glad to discuss any aspects of the command.  Hit me up!

I can see myself reading from remote file with escalation a lot - this is something you can't do with `scp`.

### Writing to a remote file as root
```
$ ssh vm1
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.5.0-25-generic x86_64)
...
Last login: Sat Dec  7 09:15:36 2024 from 10.0.2.2
mrbruno@vm1:~$ exit
logout
Connection to localhost closed.
$ echo "Welcome to vm1" | remote-file -b vm1:/etc/motd
$ ssh vm1
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.5.0-25-generic x86_64)
...
Welcome to vm1
Last login: Sat Dec  7 09:37:49 2024 from 10.0.2.2
mrbruno@vm1:~$
```

### Binary files
Binary files are not a problem.  Data is base-64 encoded in transit and integrity is preserved.  If you're reading a binary file, you probably don't want it appearing in your console but you already have to redirect anyway to it's not likely going to up on the console.  Just don't pipe it into `cat`, ok?
```
$ ssh vm1 md5sum /bin/bash
11227b11f565de042c48654a241e9d1c  /bin/bash
$ remote-file vm1:/bin/bash | md5sum 
11227b11f565de042c48654a241e9d1c  -
$
```

## Notes

- The command **must** be used as a filter - either stdin or stdout must be redirected: from or to a file or pipe.  You cannot redirect **both** since the redirection is used to determine the direction of the operation:
    - Reading from the remote system when stdout is redirected
    - Writing to the remote system when stdin is redirected
- The command relies heavily on the `ssh` command and it works best when you have configured the command to connect to the target with an ssh key so a password is not required.
