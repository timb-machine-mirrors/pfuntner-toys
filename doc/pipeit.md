# `pipeit`

## Purpose
Sends piped/redirected output to a file on a remote system

## Syntax
```
Syntax: pipeit [--verbose] system:path
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

### Argument
The destination must be expressed as `system:path` where `system` is a target suitable for `ssh` or `scp`.

## Example

```
$ head -c10000 /dev/random > random
$ md5sum random
0bed19ac814a70a23065ac4842badc75 *random
$ ls -lh random
-rw-r--r-- 1 mrbruno mrbruno 9.8K Sep 15 15:44 random
$ pipeit ubuntu:/tmp/random < random
$ ssh -q ubuntu md5sum /tmp/random
0bed19ac814a70a23065ac4842badc75  /tmp/random
$
```
Note: Since `/dev/random` produces random data, your mileage will vary.

## Notes

- `ssh` is used under the covers and it works best if you have passwordless ssh working with an ssh key
- I took pains to allow for arbitrary data so you could transmit things like compressed tarballs, images, whatever.  `base64` is used on both sides for transport.
