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

### Pushing branch to github server
While composing the bulk of the changes for this document, I deliberately did it in a feature branch to demonstrate the script:

```
    $ gitstatus --changed --untrack | xargs git add
    $ git status
    On branch git-refresh-after-merge-doc
    Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
        modified:   ../../README.md
        new file:   ../../doc/git-refresh-after-merge.md
    
    $ git commit -m 'git-refresh-after-merge doc'
    [git-refresh-after-merge-doc 8a5287f] git-refresh-after-merge doc
     2 files changed, 90 insertions(+), 51 deletions(-)
     create mode 100644 doc/git-refresh-after-merge.md
    $ git branch
      explode-changes
      fixing-superps
      freejson
    * git-refresh-after-merge-doc
      master
    $ git-push
    Enumerating objects: 8, done.
    Counting objects: 100% (8/8), done.
    Delta compression using up to 4 threads
    Compressing objects: 100% (5/5), done.
    Writing objects: 100% (5/5), 1.43 KiB | 1.43 MiB/s, done.
    Total 5 (delta 3), reused 0 (delta 0)
    remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
    remote: 
    remote: Create a pull request for 'git-refresh-after-merge-doc' on GitHub by visiting:
    remote:      https://github.com/pfuntner/toys/pull/new/git-refresh-after-merge-doc
    remote: 
    To github.com:pfuntner/toys.git
     * [new branch]      git-refresh-after-merge-doc -> git-refresh-after-merge-doc
```

### Refreshing local master branch
After pushing my branch to the github server, I did the following on github:
1. Created a pull request for my feature branch
2. Merged the pull request
3. Deleted the feature branch on github
4. Returned to my shell to run this script:

```
    $ git-log | head
    Commit                                    Author                             Date (UTC)           Text
    8a5287f629216841219c8ed0946e9b2a2edf4f24  pfuntner@pobox.com                 2022-03-12 20:08:07  git-refresh-after-merge doc
    001098b2f5e41e74016034b60e91c27205b7d067  pfuntner@pobox.com                 2022-03-12 19:55:29  Fixing typo
    470fc821c1cb344f1b4026e196c77c9d9fa2da72  pfuntner@pobox.com                 2022-03-12 19:52:50  More changes for more-head, adding it to README.md
    a49915c7ac5f8328cbb4c68442fbf8712618c3ea  pfuntner@pobox.com                 2022-03-12 19:50:12  More documentation: git-cat, char-by-char, more-head, side-d
    e798cbcbe3e8681b76a08f650b939cf3168fe7cc  pfuntner@pobox.com                 2022-03-12 15:17:11  Adding some documentation
    703463209ce70fe44d1d5488c81ebb1b5d629fa4  pfuntner@pobox.com                 2022-03-12 13:55:11  Committing changes I had laying around
    32b4399ca2a64f12a71d167999a86893151aa5f6  jpfuntne@cisco.com                 2022-03-09 15:26:23  Painting error messages in red
    3dc842e95bd945d651058ac2641a5b1a8ee12f33  jpfuntne@cisco.com                 2022-03-08 20:02:55  add option to print a full line prior to printing characters
    a9b1df043e44a6cc0e80326e9577ffbc69929ae7  jpfuntne@cisco.com                 2022-03-07 13:29:23  Merge branch 'master' of github.com:pfuntner/toys
    $ git-refresh-after-merge 
    Switched to branch 'master'
    Your branch is up to date with 'origin/master'.
    remote: Enumerating objects: 1, done.
    remote: Counting objects: 100% (1/1), done.
    remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
    Unpacking objects: 100% (1/1), 625 bytes | 625.00 KiB/s, done.
    From github.com:pfuntner/toys
       001098b..a339b7a  master     -> origin/master
    Updating 001098b..a339b7a
    Fast-forward
     README.md                      | 103 ++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------
     doc/git-refresh-after-merge.md |  38 ++++++++++++++++++++++++++++++++++++++
     2 files changed, 90 insertions(+), 51 deletions(-)
     create mode 100644 doc/git-refresh-after-merge.md
    commit a339b7a557ade5e45208f2ec25345adbea10766c
    Merge: 001098b 8a5287f
    Author: John Pfuntner <pfuntner@pobox.com>
    Date:   Sat Mar 12 15:09:16 2022 -0500
    
        Merge pull request #93 from pfuntner/git-refresh-after-merge-doc
        
        git-refresh-after-merge doc
    Master branch pulled.  Shall I remove 'git-refresh-after-merge-doc'? yes
    Deleted branch git-refresh-after-merge-doc (was 8a5287f).
    $ 
```

## Notes

- Sure, you could just issue the `git` commands to do all of this but this script makes the process less error prone and you are less likely to make a mistake or forget to do something.
