# `chars`

## Purpose
Display characters of stdin one line at a time.  This can be useful to compare long lines.

## Syntax
```
Syntax: chars [-l|--line]
```

### Options and arguments
| Option        | Description | Default                   |
|---------------| ----------- |---------------------------|
| `-l`, `--line` | Include each line before the characters for each line | The lines are not printed |

## Examples
### Example 1
When I use `diff` to compare files, often the lines are very long and there's only one character different so they're hard to spot.  Additionally, if there are multiple differences, it's difficult to know how many differences there are on a line.

This example is a little contrived but it illustrates the purpose of the command:
#### Without using `chars`
These lines aren't very long but you can already see the problem.
```
$ diff <(date) <(sleep 1; date)
1c1
< Sun 10 Apr 2022 07:52:00 AM EDT
---
> Sun 10 Apr 2022 07:52:01 AM EDT
$
```

These examples use <a href="https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html">process substitution</a> which is one of my favorite bash tricks.

#### Using `chars`

```
$ diff <(date | chars) <(sleep 1; date | chars)
24c24
< 7
---
> 8
$
```

#### Side-by-side
Using the `diff --side-by-side` option provides context.
```
$ diff --side-by-side <(date | chars) <(sleep 1; date | chars)
S								S
u								u
n								n

1								1
0								0

A								A
p								p
r								r

2								2
0								0
2								2
2								2

0								0
7								7
:								:
5								5
2								2
:								:
1								1
6							      |	7

A								A
M								M

E								E
D								D
T								T
$
```
#### Using `--line` option
```
$ diff <(date | chars -l) <(sleep 1; date | chars -l)
1c1
< Sun 10 Apr 2022 07:52:26 AM EDT
---
> Sun 10 Apr 2022 07:52:27 AM EDT
25c25
< 6
---
> 7
$
```

### A more practical example
I'll present an example of a command I might use will working on changes in a `git` repository:

```
$ diff -C10 <(git-cat master foo.py | chars) <(chars < foo.py)
```
This uses [git-cat](git-cat.md), another one of my tools, to pull out the current copy of the file in the master branch.  I've used the `diff -C` option to provide a little context of the changes.

## Notes

- The command only reads from stdin so you need to redirect input to it.

