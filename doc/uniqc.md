# `uniqc`

## Purpose
Print how many unique instances of data appear in standard input.  Along with the count of how many times each datum occurs, a percentage of the total is also displayed.  It was inspired by `sort` and `uniq -c`.  I often found myself combining those two commands and appreciated the percentage used as well.

## Syntax
```
Syntax: uniqc [FILE ...]
```

### Options and arguments

There are no options.  One or more file names can be specified to be processed.

## Examples

The examples are a little complicated so I'll break them down a little bit.  You may not be accustomed to all the other utilities and options I'm using.  I encourage you to read up on the other tools and utilities to understand what I'm doing.  If you can't figure it out, contact me and I'll try to help.

### Gauge ownership of files in my home directory

```
$ find ~ -maxdepth 1 -print0 | xargs -0 ls -ld | columns 3 | uniqc
64 total items
55  85.94% jpfuntne
 9  14.06% root
$
```
This is a rather complicated pipeline that involves another of my tools: <a href="columns.md">`columns`</a> to extract the third field from each line of `ls` output, which I happen to know is the user name of the file.  I ran this on a system which I knew ahead of time had some files owned by root.  Usually all of the files will be owned by your user but that's not the case on this system.

### Report on the file extensions

```
$ find . -type f -print0 | xargs -0 extensions | columns -F\| 2 | uniqc
17 total items
 4  23.53% txt
 3  17.65% gz
 3  17.65% out
 3  17.65% py
 1   5.88% 
 1   5.88% json
 1   5.88% tgz
 1   5.88% zip
$
```
This is another non-trivial pipeline (do you see a running theme?) that involves the use of the <a href="extensions.md">`extensions`</a> utility.  You can see the current working directory has four `*.txt` files, three `*.gz` files, etc.  One of the files also lacks an extension so that's why you see one that appears to be blank.

## Notes

- If no file names are specified on the command line, standard input will be read.  It will be an error if standard input is not redirected.
- Pipelines are your friend!  I don't think I've ever really use this outside of a pipeline.
