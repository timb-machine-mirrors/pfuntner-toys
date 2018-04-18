# `headtail`

## Purpose
This script prints out the top (aka head) and bottom (aka tail) of stdin or one or more files specified on the command line.  Along with the data, it also numbers each line.  Altogether, I like to use it to give me the sense of the data in a text file.

It was inspired by `head`, `tail`, and a combination of `wc` and `nl -ba`.

## Syntax
```
Syntax: headtail [-SIZE] [file ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-SIZE`  | Specifies the number of lines to print from stdin or the files. | Ten total lines |

## Example

```
$ ls -A
.bash_history  .cache  .gitconfig  .minttyrc  .ssh      .viminfo       c                 git          python          spark  Vagrantfile
.bash_profile  .exrc   .inputrc    .private   .vagrant  BasicDatabase  DatabaseProject1  moin         RestInterfaces  tmp
.bashrc        .gem    .lesshst    .profile   .vim      bin            django            pyinstaller  share           toys
$ ls -A | headtail
       1 .bash_history
       2 .bash_profile
       3 .bashrc
       4 .cache
       5 .exrc
         .
         .
         .
      27 share
      28 spark
      29 tmp
      30 toys
      31 Vagrantfile
$ ls -A | headtail -4
       1 .bash_history
       2 .bash_profile
         .
         .
         .
      30 toys
      31 Vagrantfile
$
```

## Notes

- If no files are specified on the command line, the script needs to read from stdin and if it is not redirected, an error is raised.
- The _middle portion_ of each file (which doesn't get printed) is represented by three period as a kind of ellipsis.  If the file's length is less than or equal to the number of lines desired, no ellipsis is printed.
