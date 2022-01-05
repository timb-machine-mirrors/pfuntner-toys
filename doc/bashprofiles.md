# `bashprofiles`

## Purpose
Reports on existence of `bash` profiles for the user.

Most people know that the bash shell supports a user profile but some people don't know that bash supports various file names and uses the first one that it finds in a defined order. Personally, I can never remember all the file names exactly, don't remember the order in which the shell searches, and often can't remember the file used for a particular system. 

I've tried to address the problem with this script - it knows the exact names the shell looks for and in what order it looks for them. By default, it will just tell you the profile bash will use for you, even if you have two or more to choose from. One of my favorite ways to use the default behavior is to edit my profile file. I don't care what the name is - just edit it!

```
$ vi $(bashprofiles)
```

## Syntax
```
Syntax: bashprofiles [--all]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `--all`  | Report on all files.  The script reports on all files in the order the shell looks for them. Even if you don't have the file, the script tells you so.  | Only the first file that the script finds is printed. |

## Example

```
$ bashprofiles
/home/mrbruno/.profile
$ bashprofiles --all
You do not have /home/mrbruno/.bash_profile
You do not have /home/mrbruno/.bash_login
You have /home/mrbruno/.profile
$ 
```

## Notes

- You might need to use quotes to protect blanks in the path name reported by the script.  Generally blanks are discouraged in paths on Unix but they are more common on Windoze, especially in name of a user's home directory.

  ```
  $ bashprofiles
  /home/John Doe/.bash_profile
  $ wc $(bashprofiles)                                   # blank is not protected
  wc: /home/John: No such file or directory
  wc: Doe/.bash_profile: No such file or directory
  0 0 0 total
  $ wc "$(bashprofiles)"                                 # blank is protected
    52  251 1686 /home/John Doe/.bash_profile
  $
  ```

  This solution might not work for all cases.  If someone decided to use the name _John O'Doe_, the embedded quote would probably confuse the shell.
