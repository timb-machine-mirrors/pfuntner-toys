# `git-clone`

## Purpose
Clones a git repository.

## Syntax
```
Syntax: git-clone [-u [USER]] [--http] [-d] [-v] repo [repo ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-u USER` or `--user USER` | Use an alternate Github user | Use the `$GITHUB_USER` environment variable (if it's defined) or your login userid |
|  `-h` or `--http` | Use an http-style Github URL | Use an ssh-style Github URL |
|  `-d` or `--dry-run` | Do not execute the `git clone` command | Execute the `git clone` command |
|  `-v` or `--verbose` | Enable verbose debugging | Debugging is not enabled |

## Example

```
$ git-clone -u pfuntner toys
git clone git@github.com:pfuntner/toys.git
Cloning into 'toys'...
$ ls toys
ansible  bin  _config.yml  doc	images	__init__.py  misc  README.md  test
$ 
```

I could have done this without the `-u` option but I wanted to show a command that would work for more people.

## Notes

- This is a very simple command and you can certainly go to the desired repository and copy the statement from there.  Or if you have a great memory, you can type if from memory.  I don't know about anyone else but I have better things to remember.  I find my command much easier.
- I typically add `export GITHUB_USER=pfuntner` to my `~/.profile` because my id can vary depending on the system I'm on.
- ssh-style Github URLs expect you have already shared your public ssh key on Github _(Settings -> SSH and GPG keys)_.  http-style URLs can work just as well to clone a repo but if you try to make changes to the remote repo on Github, you'll be challenged for your Github credentials. 