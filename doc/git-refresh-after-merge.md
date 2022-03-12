# `git-refresh-after-merge`

## Purpose
The purpose of the script is pretty self-explanatory.  Here's a use case while working in a collaborative development team:
1. You have created a _feature branch_ with changes
2. You've merged the branch into the master/main branch
3. You want to refresh your local master branch and remove the old feature branch

This script does all of that without you having to think too much about it:
1. Does `git checkout master` or `git checkout main` (whichever is appropriate)
2. Does `git pull` on the master/main branch
3. Displays the top commit (which should be what you merged)
4. Asks for your permission to remove your feature branch
5. Removes the feature branch if you have granted your permission

If anything goes wrong during any of the above steps, the script stops and doesn't perform any more commands.  For example, if you have outstanding changes in your feature branch, `git checkout master` will likely fail and cause the script to abort.

## Syntax
```
Syntax: git-refresh-after-merge
```

### Options and arguments
There are no options or arguments.

## Example

While composing the bulk of the changes for this document, I deliberately did it in a feature branch to demonstrate the script:

```
$ template
This is a template.  Please fill in the details and rock on.
$ 
```

## Notes

- Sure, you could just issue the `git` commands to do all of this but this script makes the process less error prone and you are less likely to make a mistake or forget to do something.
