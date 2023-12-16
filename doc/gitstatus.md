# `gitstatus`

## Purpose
Display files in a local git repository that have changes, are not tracked, etc.

I know, you're saying to yourself _What? Isn't that what `git status` is for?!_  Well, sure, but the output isn't always the easiest to read, and more importantly, reuse.  This script actually calls `git status` and processes the output to do what it does.  The biggest purpose I have for the script is to add files to my git repository.  I can commit files easier when I combine this command with `git add`.  Check out the examples I've provided.

## Syntax
```
Syntax: gitstatus [-h] [-u] [-l] [-v] [args ...]
```

#### Arguments
Zero or more arguments may follow any options (if there are any).  These are passed directly to `git status` to change the scope of files being considered.

### Options and arguments
| Option             | Description               | Default                                     |
|--------------------|---------------------------|---------------------------------------------|
| `-u` `--untracked` | Report on untracked files | Untracked files are not reported by default |
| `-l` `--long`      | Long output style         | Short output style is the default           |
| `-v` `--verbose`   | Debugging                 | Debugging is not turned on by default       |
| `-h` `--help`      | Print online help         | Help is not provided by default             |

## Examples

### Simple file adds and changes
```
$ date >> README.md 
$ date > new-file
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	new-file

no changes added to commit (use "git add" and/or "git commit -a")
$ gitstatus 
2023-12-16 11:15:11,770 WARNING /home/mrbruno/bin/gitstatus:61 Untracked file 'new-file'
README.md
$ gitstatus --untracked
new-file
README.md
$ gitstatus --untracked | xargs -r echo git add
git add new-file README.md
$ gitstatus --untracked | xargs -r git add
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   README.md
	new file:   new-file

$ 

```

### Rebasing
```commandline
$ git rebase main
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
error: could not apply 323bb97... foo
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
Could not apply 323bb97... foo
$ git status
interactive rebase in progress; onto 681a2e3
Last command done (1 command done):
   pick 323bb97 foo
No commands remaining.
You are currently rebasing branch 'foo' on '681a2e3'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
$ gitstatus
2023-12-16 11:30:51,568 WARNING /home/mrbruno/bin/gitstatus:38 Rebase in progress!
2023-12-16 11:30:51,569 WARNING /home/mrbruno/bin/gitstatus:44 There are rebase conflicts
README.md
$ vi $(gitstatus) # I am resolving the conflict
2023-12-16 11:30:55,539 WARNING /home/mrbruno/bin/gitstatus:38 Rebase in progress!
2023-12-16 11:30:55,539 WARNING /home/mrbruno/bin/gitstatus:44 There are rebase conflicts
$ gitstatus
2023-12-16 11:31:04,765 WARNING /home/mrbruno/bin/gitstatus:38 Rebase in progress!
2023-12-16 11:31:04,766 WARNING /home/mrbruno/bin/gitstatus:44 There are rebase conflicts
README.md
$ gitstatus | xargs git add
2023-12-16 11:31:21,564 WARNING /home/mrbruno/bin/gitstatus:38 Rebase in progress!
2023-12-16 11:31:21,565 WARNING /home/mrbruno/bin/gitstatus:44 There are rebase conflicts
$ gitstatus
2023-12-16 11:31:29,905 WARNING /home/mrbruno/bin/gitstatus:38 Rebase in progress!
2023-12-16 11:31:29,905 WARNING /home/mrbruno/bin/gitstatus:112 No files to stage but ready to continue rebase: README.md
$ git rebase --continue
[detached HEAD e041c01] foo
 1 file changed, 1 insertion(+), 1 deletion(-)
Successfully rebased and updated refs/heads/foo.
$ git status
On branch foo
nothing to commit, working tree clean
$ gitstatus
2023-12-16 11:32:02,444 WARNING /home/mrbruno/bin/gitstatus:121 No changes
$ 
```
It's not really necessary to do some of the `git status` commands but it's a good practice to assure yourself you and git are _on the same page_. 

## Notes

- Relies a lot on `git status --short ...`
