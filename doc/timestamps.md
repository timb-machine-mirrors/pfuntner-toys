# `timestamps`

## Purpose
Show timestamps of files, sorted with the most recently modified first.

## Syntax
```
Syntax: timestamps [-h] [-n | -e] [filename [filename ...]]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-n`, `--nameonly`  | Display name only | Display filename and time |
|  `-e`, `-d`, `--elapsed`, `--duration`  | Display elapsed time from file modification | Display time of most recent modification |

#### Arguments
Files can be specified as arguments on the command line or fed via stdin.

## Example

```
$ timestamps * | head
2019/02/17 08:33:51.669163 pycomment
2019/02/16 17:38:37.323349 keytest
2019/02/16 17:29:55.118344 SecureKeyValues.pyc
2019/02/16 16:18:24.270556 fernet
2019/02/16 16:00:42.712275 timer
2019/02/16 08:23:44.163150 needsdoc
2019/02/16 08:06:49.685257 BrunoUtils.pyc
2019/02/16 08:06:49.681257 Decolorizer.pyc
2019/02/16 07:10:38.144313 viswap
2019/02/10 08:59:29.446273 recentdownloads
$ ls | timestamps -e | head
0:11:10.698431 pycomment
15:06:25.044245 keytest
15:15:07.249250 SecureKeyValues.pyc
16:26:38.097038 fernet
16:44:19.655319 timer
1 day, 0:21:18.204444 needsdoc
1 day, 0:38:12.682337 BrunoUtils.pyc
1 day, 0:38:12.686337 Decolorizer.pyc
1 day, 1:34:24.223281 viswap
6 days, 23:45:32.921321 recentdownloads
$ 
```

I did take the liberty of removing some error messages from the script when `head` prevents it from writing more than 10 lines.

## Notes

- Commands such as `ls -lt` can do some of what this script does but this script does it a little more easily.
- For files with a timestamp in the future (see [`touch -t`](http://pubs.opengroup.org/onlinepubs/7908799/xcu/touch.html)), a negative elapsed time is shown.