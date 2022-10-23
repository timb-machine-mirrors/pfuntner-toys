# `install-python`

## Purpose
A simple tool to install Python in a Docker container or remote host for general user if necessary.  Typically:
- Alpine containers don't have Python installed
- Redhat machines often don't have Python in a _usual_ location

I use Ansible a lot but Ansible is not possible if Python isn't present on the target.  So sometimes I'll use this tool before running an Ansible playbook on the target.

## Syntax
```
Syntax: install-python [--verbose] [-d] [-p PROXY] [--dry-run] [-q] host ...
```

### Options and arguments
| Option           | Description                                                                                                              | Default                                      |
|------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| `-d`, `--docker` | Use `docker exec` to access host as Docker container                                                                     | The default is to access the hosts via `ssh` |
| `-p`, `--proxy`  | Use a proxy with package manager                                                                                         | The default is not to use a proxy            |
| `--dry-run`      | Do not make any changes - just show what changes would be done.  This could be a good way to tell if Python is available | The default is to install Python             |
| `-q`, `--quiet`  | Use the `ssh -q` option to reduce noise.  Not applicable with `--docker`                                                 | The default is to install Python             |
| `-v`             | Enable verbose debugging                                                                                                 | Debugging is not enabled                     |

## Example

```
$ docker run -dit --rm --name alpine alpine
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
213ec9aee27d: Pull complete 
Digest: sha256:bc41182d7ef5ffc53a40b044e725193bc10142a1243f395ee852a8d9730fc2ad
Status: Downloaded newer image for alpine:latest
fba44ceda245255655253de5d0c2a5abc514f95048f2e63679e60fe2c0a2fd02
$ install-python --dry-run --docker alpine
2022-10-22 07:41:52,075 WARNING /home/mrbruno/bin/install-python:75 Skipping ['docker', 'exec', 'alpine', 'sh', '-c', 'apk add python3'] because of --dry-run

# this will show all the commands used to probe the container
$ install-python -v --dry-run --docker alpine
2022-10-22 07:42:12,940 INFO /home/mrbruno/bin/install-python:171 alpine: alive
2022-10-22 07:42:13,012 INFO /home/mrbruno/bin/install-python:130 alpine: could not find python
2022-10-22 07:42:13,080 INFO /home/mrbruno/bin/install-python:130 alpine: could not find python3
2022-10-22 07:42:13,152 INFO /home/mrbruno/bin/install-python:32 alpine: installing python3
2022-10-22 07:42:13,152 WARNING /home/mrbruno/bin/install-python:75 Skipping ['docker', 'exec', 'alpine', 'sh', '-c', 'apk add python3'] because of --dry-run

$ install-python --docker alpine
alpine: After installing Python 3, /usr/bin/python3: Python 3.10.5
$ install-python --dry-run --docker alpine
alpine: /usr/bin/python3: Python 3.10.5
$ install-python -v --dry-run --docker alpine
2022-10-22 07:42:48,986 INFO /home/mrbruno/bin/install-python:171 alpine: alive
2022-10-22 07:42:49,065 INFO /home/mrbruno/bin/install-python:130 alpine: could not find python
alpine: /usr/bin/python3: Python 3.10.5
$ 
```

## Notes

- If Python is installed, the tool will **not** set up a symbolic link for `/usr/bin/python`.  Likely, `python3` is in the host's `$PATH`.
- When using `ssh`, it works best if you have set up password-less access with `ssh` keys.
- In my experience, newly-installed Redhat machines have Python in a weird location such as `/usr/libexec/platform-python`.  Ansible can usually locate and use this interpreter but it's awkward for general use and I've never seen that directory in a user's `$PATH`.