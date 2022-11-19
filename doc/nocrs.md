# `nocrs`

## Purpose
Remove carriage returns from files.  This is especially useful for files created on Windoze that have carriage returns - one of the worst things about Windoze, in my opinion.

## Syntax
```
Syntax: nocrs [-v] file ...
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`, `--verbose`  | Increase debugging messages.  More instance of this option produce more debugging. | Debugging is not enabled |

#### Arguments
Each file to process is specified as an argument on the command line.

## Example

```
$ echo -e 'This is a test\r' > test
$ od -ctx1 test
0000000   T   h   i   s       i   s       a       t   e   s   t  \r  \n
         54  68  69  73  20  69  73  20  61  20  74  65  73  74  0d  0a
0000020
$ nocrs test
test
$ od -ctx1 test
0000000   T   h   i   s       i   s       a       t   e   s   t  \n
         54  68  69  73  20  69  73  20  61  20  74  65  73  74  0a
0000017
$
```

```
$ echo -e 'This is a test\r' > test
$ nocrs -v test
2019-02-17 10:23:56,404 INFO /home/mrbruno/bin/nocrs:45 processing test
2019-02-17 10:23:56,404 INFO /home/mrbruno/bin/nocrs:25 Backing up 'test' to '.test-20190217102356'
test
$
```

## Notes

- The script writes to the original files when carriage returns are present.
- The script backups up the original file (see the example) using `cp -pv` to preverse the file in case there are issues
- If a file does not contain carriage returns, there are no changes and the file is not backed up.
- A great example of using this tool is Python scripts.  Python on Unix will not be able to process the script!

  ```
  $ cat test.py
  #! /usr/bin/env python
  print "Hello, Python world"
  $ od -ctx1 test.py
  0000000   #   !       /   u   s   r   /   b   i   n   /   e   n   v
           23  21  20  2f  75  73  72  2f  62  69  6e  2f  65  6e  76  20
  0000020   p   y   t   h   o   n  \r  \n   p   r   i   n   t       "   H
           70  79  74  68  6f  6e  0d  0a  70  72  69  6e  74  20  22  48
  0000040   e   l   l   o   ,       P   y   t   h   o   n       w   o   r
           65  6c  6c  6f  2c  20  50  79  74  68  6f  6e  20  77  6f  72
  0000060   l   d   "  \r  \n
           6c  64  22  0d  0a
  0000065
  $ chmod +x test.py
  $ ./test.py
  /usr/bin/env: ‘python\r’: No such file or directory
  $ python test.py
  Hello, Python world
  $
  ```
