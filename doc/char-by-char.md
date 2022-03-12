# `char-by-char`

## Purpose
Display characters from a file character-by-character, each on a separate line.

## Syntax
```
Syntax: char-by-char [--verbose] [--long]
```

### Options and arguments
| Option       | Description | Default |
|--------------| ----------- | ------- |
| `-l` `--long` | Print line prior to individual characters | Only characters are printed |
| `-v`         | Enable verbose debugging | Debugging is not enabled |

## Examples
### Simple example
```
$ date > file1
$ date > file2
$ diff file1 file2
1c1
< Sat 12 Mar 2022 10:46:56 AM EST
---
> Sat 12 Mar 2022 10:46:58 AM EST
$ diff <(char-by-char < file1) <(char-by-char < file2)
24c24
< 6
---
> 8
$ diff --side-by-side <(char-by-char < file1) <(char-by-char < file2)
S								S
a								a
t								t
 								 
1								1
2								2
 								 
M								M
a								a
r								r
 								 
2								2
0								0
2								2
2								2
 								 
1								1
0								0
:								:
4								4
6								6
:								:
5								5
6							      |	8
 								 
A								A
M								M
 								 
E								E
S								S
T								T
$ 
```
Note that when I didn't use `char-by-char`, I know there's a difference but it's so subtle that it's hard to pick it out.  It can be tedious to the extreme to look at each character yourself.

The example above makes use of one of my very favorite bash _tricks_: [Process Substitution](https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html):

    <(command)
Basically what the shell does is that it executes `command` and directs the output to a temporary file.  What bash substitutes on the command line is a filename, often something like `/dev/fd/63`.  This is all done under the covers and you don't have to worry about cleaning up the file.

### A more complicated example
One of the use cases for which I created the script is to compare changes I'm making to a file in a git repository.  Sure, `git diff` has its uses but if you're doing surgery on a long line and online changing a few thing on the line, you need to do a character-by-character comparison:

    $ sidediff --wide <(git-cat master filename | grep-cat '/regexp/' | char-by-char) \
    <(cat filename | grep-cat '/regexp/' | char-by-char)

[`sidediff`](side-diff.md), [`git-cat`](git-cat.md), and [`grep-cat`](grep-cat.md) are other tools of mine in this repository:

- I'm using `grep-cat` to pull out specific lines of the file using an _eye-catcher_ pattern I know is fairly unique and will find the lines in both the before and after versions of the file. 
- I used `cat` to read the new version of the file but I didn't really need to do that.  I could have redirected the file directly into `grep-cat` instead of using a pipeline but doing it this way was more consistent with the old verison of the file and it's easier to compose the command this way.  

## Notes

- The script is not very useful when it's not used in combination with other commands.  The example is an excellent use case and you can get much more complicated.
- This can be highly useful comparing files.  Often, differences can be very minor and it helps to look at the changes file-by-file.
- The script only read from stdin so you must redirect input or use the script in a pipeline.
