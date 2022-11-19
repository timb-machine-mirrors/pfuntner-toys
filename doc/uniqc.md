# `uniqc`

## Purpose
Print how many unique instances of data appear in standard input.  Along with the count of how many times each datum occurs, a percentage of the total is also displayed.  It was inspired by `sort` and `uniq -c`.  I often found myself combining those two commands and appreciated the percentage used as well.

## Syntax
```
Syntax: uniqc [-f|--fifo] [FILE ...]
```

### Options and arguments

| Option | Description | Default |
| ------ | ----------- | ------- |
| `-f` or `--fifo` | List lines in the order they first appeared | By default, the script prints lines in descending occurrence |

One or more file names can be specified to be processed.

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
$ find . -type f -print0 | xargs -0 extensions | columns -F \| 2 | uniqc
273 total items
 97  35.53%
 84  30.77% gz
 40  14.65% jpg
 32  11.72% out
  4   1.47% pdf
  4   1.47% py
  4   1.47% txt
  1   0.37% base64
  1   0.37% deb
  1   0.37% java
  1   0.37% json-sample
  1   0.37% md
  1   0.37% odt
  1   0.37% png
  1   0.37% xls
$
```
This is another non-trivial pipeline (do you see a running theme?) that involves the use of the <a href="extensions.md">`extensions`</a> utility.  You can see the current working directory has eighty-four `*.gz` files, forty `*.jpg` files, etc.  Many of the files also lack an extension so that's why you see ninety-seven appear to be blank.

### Show most recently updates files in git

```
$ gitfiles | columns -- -1 | uniqc --fifo | headtail
       1 1200 total items
       2    2   0.17% misc/zaci-20/setup
       3    2   0.17% bin/assassinate
       4   10   0.83% doc/columns.md
       5    1   0.08% bin/delete_docker_images
         .
         .
         .
     432    3   0.25% git.json-sample
     433    3   0.25% htmlize
     434    3   0.25% longjson
     435    3   0.25% timestamp
     436    2   0.17% git.json
$
```

So the most recently updated file was `misc/zaci-20/setup`.  Since this is the most recently updated, I have a good memory of it at the time of the update - I actually **deleted** the file so you won't find it in the repo any longer unless you look at old commits.

You'll notice that I use three other scripts of mine: `gitfiles` (_I haven't been inspired to do doc for that yet_), [`columns`](columns.md), and [`headtail`](headtail.md).

In this example, I'm not so interested in the number of times a file occurred but the info

Gee, another pipeline! :-)

## Notes

- If no file names are specified on the command line, standard input will be read.  It will be an error if standard input is not redirected.
- Pipelines are your friend!  As [Tommy Flanagan](https://www.wikiwand.com/en/Recurring_Saturday_Night_Live_characters_and_sketches_introduced_1985%E2%80%931986#/Tommy_Flanagan,_the_Pathological_Liar) might say: **_Get to know them!_** I don't think I've ever really use this outside of a pipeline.
