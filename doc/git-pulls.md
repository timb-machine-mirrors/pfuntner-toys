# `git-pulls`

## Purpose
Perform `git pull` over one or more git repositories.

By default, it will only try to do `git pull` in a repository if the current branch is master or main.  If the repo is some feature branch, it will not do `git pull` unless you override the behavior.

## Syntax
```
Syntax: git-pulls [-verbose] [--dry-run] [---branch] [root]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-d` or `--dry-run`  | Print information but do not do `git pulls` | The default is to do `git pull` on all the repos |
|  `-b` or `--branch`  | Do not ignore repos not in the master/main branch | The tool does not do `git pull` if the repo is not in the master or main branch |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `root` | Specifies the directory in which to look for repositories | `~/repos` |

## Example

### Dry-run
```
$ git-pulls --dry-run
2022-05-26 12:02:19,396 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/bruno-ansible' ('/home/jpfuntne/repos/bruno-ansible')
2022-05-26 12:02:19,396 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:19,898 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:20,460 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/bruno-ansible', 'master', 'b1452a9', '2022-05-17 06:54:19', 'Creating playbook to', '', '', '']
2022-05-26 12:02:20,462 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/cisco-pfuntner' ('/home/jpfuntne/repos/cisco-pfuntner')
2022-05-26 12:02:20,462 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:21,201 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:21,495 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/cisco-pfuntner', 'master', 'afdaa3d', '2022-05-24 10:37:05', 'Addressing issues fo', '', '', '']
2022-05-26 12:02:21,496 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/docker' ('/home/jpfuntne/repos/docker')
2022-05-26 12:02:21,496 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:21,548 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:21,605 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/docker', 'master', '6f4160e', '2019-09-13 13:42:54', 'I got the makefile t', '', '', '']
2022-05-26 12:02:21,606 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/fun' ('/home/jpfuntne/repos/fun')
2022-05-26 12:02:21,607 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:21,682 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:21,773 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/fun', 'master', '96fb36e', '2022-05-10 15:01:51', 'Trying setting of ne', '', '', '']
2022-05-26 12:02:21,774 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/only-bruno' ('/home/jpfuntne/repos/only-bruno')
2022-05-26 12:02:21,774 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:21,838 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:21,901 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/only-bruno', 'main', 'f34654f', '2021-11-09 10:30:46', 'adding title, main h', '', '', '']
2022-05-26 12:02:21,902 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/pfuntner.github.io' ('/home/jpfuntne/repos/pfuntner.github.io')
2022-05-26 12:02:21,903 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:21,962 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:22,026 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/pfuntner.github.io', 'master', '40d3412', '2020-11-07 09:05:29', 'Creating separate st', '', '', '']
2022-05-26 12:02:22,026 INFO /home/jpfuntne/bin/git-pulls:109 Processing '/home/jpfuntne/repos/toys' ('/home/jpfuntne/repos/toys')
2022-05-26 12:02:22,027 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'branch']
2022-05-26 12:02:22,089 INFO /home/jpfuntne/bin/git-pulls:18 Executing ['git', 'log', '-1']
2022-05-26 12:02:22,168 INFO /home/jpfuntne/bin/git-pulls:133 cols: ['/home/jpfuntne/repos/toys', 'master', 'e46584a', '2022-05-24 15:08:28', 'Adding more potentia', '', '', '']
2022-05-26 12:02:22,169 INFO /home/jpfuntne/repos/toys/bin/table.py:583 args.rotate: False, order: ('Path', 'Branch', 'Old SHA1', 'Old Date', 'Old Text', 'New SHA1', 'New Date', 'New Text')
Path                                     Branch  Old SHA1  Old Date             Old Text              New SHA1  New Date  New Text
/home/jpfuntne/repos/bruno-ansible       master  b1452a9   2022-05-17 06:54:19  Creating playbook to
/home/jpfuntne/repos/docker              master  6f4160e   2019-09-13 13:42:54  I got the makefile t
/home/jpfuntne/repos/fun                 master  96fb36e   2022-05-10 15:01:51  Trying setting of ne
/home/jpfuntne/repos/pfuntner.github.io  master  40d3412   2020-11-07 09:05:29  Creating separate st
/home/jpfuntne/repos/toys                master  e46584a   2022-05-24 15:08:28  Adding more potentia
$
```
I honestly don't use `--dry-run` very often.  If I had it to do over again, I would do it differently.  Perhaps it would be more useful and I would actually use it more!
- I don't think the debugging messages are necessary.  I think I would get rid of them from `--dry-run`.  They are still available through `--verbose`.
- I would strive to actually go to the remote server and see what's actually available.  I don't think it does that right now and that's a shame.

### Live run
I didn't have any commits I was aware of needing.  While working on this documentation, I pushed it while _halfway-done_ and used `git-pulls` on another machine to freshen it.
```
$ git pulls
***************************
* /home/ubuntu/repos/toys *
***************************
Updating e46584a..d24e741
Fast-forward
 doc/git-pulls.md | 81 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 81 insertions(+)
 create mode 100644 doc/git-pulls.md
From github.com:pfuntner/toys
   e46584a..d24e741  master     -> origin/master
Path                               Branch  Old SHA1  Old Date             Old Text              New SHA1  New Date             New Text
/home/ubuntu/repos/fun             master  96fb36e   2022-05-10 15:01:51  Trying setting of ne
/home/ubuntu/repos/toys            master  e46584a   2022-05-24 15:08:28  Adding more potentia  d24e741   2022-05-26 12:15:45  Preliminary doc for
/home/ubuntu/repos/bruno-ansible   master  b1452a9   2022-05-17 06:54:19  Creating playbook to
/home/ubuntu/repos/examples        master  c1ba3dc   2022-01-24 12:27:39  Create README.md
$
```
Again, if I had it to do over, I think I might get rid of all the nonsense at the start and make it more silent if it's there are no errors or unexpected behavior.

## Notes

- There are a few reasons I use this script:
    - I typically have the same repos cloned on various machines so they're not hard to get out of sync if I don't do `git pull` on them.  I usually have four or more (see above) repos on each machine and I don't like to have to think or do a lot of unnecessary keystrokes.
    - In my full-time job, I work on a team where we have literally a couple of dozen repos.  It would drive me crazy to freshen them all up manually so I love to use the script there.
- I've gotten into the habit of using hyphens a lot in my script names.  This is rather fortunate in this case because the standard `git` command is _smart enough_ to be able to accept `git pulls`, equate that to `git-pulls`, and run my script just by virtue of the fact that the script is in my `$PATH`.  Some might say that's a bad thing but I like it.
- I typically clone all of my _working_ repos into `~/repos` so that's the reason for the default value of the `root` argument.  I don't know how common this is but I think it's a good practice.
- I sometimes forget the style of the argument and need to use _trial-and-error_.  For example, `~/repos` is fine usually for me but sometimes I want to target repos in another directory I'm not sure if I need to specify the parent directory (`.` or some other relative or absolute path) or one or more of the actual repositories.  I go back and forth about which to use.  If I had it to do over again, I might allow it to work either way and just seek out any directory that has a `.git` directory.  Perhaps I'll go back and work on this.
