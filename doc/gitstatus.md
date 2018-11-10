# `gitstatus`

## Purpose
Display files in a local git repository that have changes, are not tracked, etc.

I know, you're saying to yourself _What? Isn't that what `git status` is for?!_  Well, sure, but the output isn't always the easiest to read, and more importantly, reuse.  This script actually calls `git status` and processes the output to do what it does.  The biggest purpose I have for the script is to add files to my git repository.  I can commit files easier when I combine this command with `git add`.  Check out the examples I've provided.

## Syntax
```
Syntax: gitstatus [-c|-m|--changes|--changed|modified] [-u|--untracked] [FILE|DIR ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-c`, et al  | Changed files | Reporting on changed files is the default.  There are several synonymous options because I don't like having to remember a single option. |
|  `-u`, et al  | Untracked files | Report on untracked files. |

#### Arguments
Zero or more arguments may follow any options (if there are any).  These are passed directly to `git status` to change the scope of files being considered.

## Examples

```
~/toys/bin$ gitstatus # I changed the top README file and made some additions to the .gitignore file
../.gitignore
../README.md
~/toys/bin$ gitstatus -u # I have several untracked files - most I have no intent on committing to the remote repo for now
bruno-service-control
move
needsdoc
perline
unhex
whochat
../doc/gitstatus.md
~/toys/bin$ gitstatus -u ../doc # this restricts the status to only the documentation files
../doc/gitstatus.md
~/toys/bin$ gitstatus
../.gitignore
../README.md
~/toys/bin$ gitstatus -u
bruno-service-control
move
needsdoc
perline
unhex
whochat
../doc/gitstatus.md
~/toys/bin$ gitstatus -u ../doc
../doc/gitstatus.md
~/toys/bin$ git add -v $(gitstatus) $(gitstatus -u ../doc)
add '.gitignore'
add 'README.md'
add 'doc/gitstatus.md'
~/toys/bin$ 
```

## Notes

- Options can be combined to report on untracked and changed files together but I didn't have a good example handy for doing that.
- The last example uses the `-v` option of `git add`.  Usually I don't do that but the default behavior doesn't typically produce output unless there are errors.  By using the option, I've demonstrated what is being added.
- My most common use of this command is: `git add $(gitstatus)`
- The script only works with changed and untracked files and there might be some cases when that doesn't do what you really want, for instance maybe during rebasing.  I'll likely expand the command as time goes and I use the script in more situations.
