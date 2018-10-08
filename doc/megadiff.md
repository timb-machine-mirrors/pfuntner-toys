# `megadiff`

## Purpose
Compare files under two directories.

## Syntax
```
Syntax: megadiff [-x|--exclude regexp ... ] dir1 dir2
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-x`  | Exclude files | Exclude files that match the regular expression.  Multiple regular expressions can be specified using two or more sets of options and arguments. |

## Example

Here are some commands that compare two `git` repo trees with each other:

```
$ megadiff -x '^.git$' megadiff/dir* | headtail
       1 match megadiff/dir1/toys/.gitignore megadiff/dir2/toys/.gitignore
       2 match megadiff/dir1/toys/README.md megadiff/dir2/toys/README.md
       3 match megadiff/dir1/toys/__init__.py megadiff/dir2/toys/__init__.py
       4 match megadiff/dir1/toys/bin/BrunoUtils.py megadiff/dir2/toys/bin/BrunoUtils.py
       5 match megadiff/dir1/toys/bin/Data.py megadiff/dir2/toys/bin/Data.py
         .
         .
         .
     168 match megadiff/dir1/toys/misc/.exrc megadiff/dir2/toys/misc/.exrc
     169 match megadiff/dir1/toys/misc/.profile megadiff/dir2/toys/misc/.profile
     170 match megadiff/dir1/toys/misc/zaci-20/setup megadiff/dir2/toys/misc/zaci-20/setup
     171 match megadiff/dir1/toys/test/__init__.py megadiff/dir2/toys/test/__init__.py
     172 match megadiff/dir1/toys/test/jsonhunt.py megadiff/dir2/toys/test/jsonhunt.py
$ megadiff -x '^.git$' megadiff/dir* | columns 1 | uniqc
172 total items
171  99.42% match
  1   0.58% md5sum-mismatch
$ megadiff -x '^.git$' megadiff/dir* | grep -v ^match
md5sum-mismatch megadiff/dir1/toys/bin/megadiff megadiff/dir2/toys/bin/megadiff
$
```

### Notes
1. Since I know I'm comparing `git` repo trees, I avoid files in the `.git` directory in each tree.
2. The first command shows several files that match.  It almost looks as though everything matches.
3. The second command shows how many files matched and how many did not - and if not, how they failed.
4. I know there's one mismatch so the third command prints only the mismatch.

## Notes

- The expected result for each file is one of the following:

  | result | description |
  | ------ | ----------- |
  | `match` | The files are identical |
  | `md5sum-mismatch` | The files have different checksums and their content is presumably different |
  | `type-mismatch` | The files are no the same type |
  | `missing` | One tree has a file that the other tree does not.  Either the first file is `None` or the second one is |

- The script makes sure files of the same name are both regular files or both directories.  If each file is another type of file (such as a _character special_ file like `/dev/null`), the script raises an exception.  I could only find an easy way to compare file types of in Python if they were regular files or directories.  I could probably do an `ls` under the covers but don't want to do that.
- Admittedly, `diff -r` could do a lot of this but I wanted to do it in my own tool and control the processing using regular expressions to exclude various files
