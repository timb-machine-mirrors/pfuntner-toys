# `git`

## Purpose
No, I didn't re-write `git`!! This is a front-end to `/usr/bin/git` which supplies my github user & token for prompts. I created this because of I got sick of having to enter the token myself. Also, I have to have the presence of mine to get my token every time! I have it stored in a file in my home directory but I had to cat it every time I wanted to use a `git` command! This solves the problem for the most part.

## Syntax
```
Syntax: git ...
```

### Options and arguments
The are no special options or arguments introduced by the script but a plethora of them are supported by the real `git` utility.

## Example
There isn't much to show. Just use the script instead of `git` directly.  You might notice that `git` prompts for your user and password for some operations and they are provided automatically.

## Notes
- Instead of putting `$HOME/bin` early in my `$PATH`, I usually just create a shell alias for `git` which leads to my script.
- The script is **not perfect!** There are some instances where `git` wants to do something interactively with me and the script just hangs because it doesn't expect such a prompt. Often, there isn't even any warning before the hang. If I get the sense that the script is hanging, I have to cancel it, get my token, and re-issue the command with an absolute path to `/usr/bin/git` to see what it was really doing.  It often happens when `git` needs to merge updates from the server into your clone of the repo and it's launched `vi` to provide some details about the merge.  Maybe there's a way avoid this but I haven't explored that yet.
- The [`pexpect`](https://pexpect.readthedocs.io/en/stable/) Python module is required to field the prompts from the real `git` utility and supply responses.
- `git.json` is used to store the git user & token and supports multiple servers each its own user & token.  
  - The file must be in the same directory as this script.
  - A template for the file is provided in `git.json-sample`.  You need to copy the file to `git.json` and update the user/token, adding additional repos if desired.
  - Only one user and token is supported for each unique server.
  - I recognize that the file is insecure but I haven't tried to make changes to make it more secure.  Since I first created this, I have dealt with sensitive information in other scripts better but it requires a passphrase created by the user.  I rather like that the script doesn't prompt for a password... that's kind of the whole point!  But seriously, if you make use of `git` tokens, how do you deal with them?  I think that going to the github website every time is cumbersome.  So there are advantages and disadvantages to this script its JSON file.
