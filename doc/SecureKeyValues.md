# `SecureKeyValues`

## Purpose
Manages secure stores, providing storage and access to sensitive information such as passwords and login keys in encrypted files.

There is support for invoking the script directly from the command line but you can also load it as a Python class and use methods get a key.

## Syntax
```
Syntax: SecureKeyValues.py [-h] 
                           [-s STORENAME]
                           [-k KEY | --ssh] 
                           [-j] 
                           [-v]
                           -o {read,get,set,remove,test} 
                           [arg [arg ...]]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-s`, `--store` | The name of the secure store file.   For a simple name without a slash such as `foo`, this translates to path `$HOME/.private/foo`.  If the name starts with a slash, it specifies the absolute pathname to the file.  If the file has a slash but it's not the first character, argument is a filename relative to the current working directory. | Required for `read`, `get`, `set`, and `remove` operations. |
| `-k`, `--key` | The encryption key.  It's up to you but I think it's a bad idea to provide the key as an argument because it will be visible to other users in the output from the `ps` command. | There is no default key.  If it is not specified, it will be prompted for without echoing the key. |
| `-ssh` | Use your private rsa SSH key (`$HOME/.ssh/id_rsa`) as the encryption key | There is no default key |
| `-j`, `--json` | Display output in JSON form. | The output is to print keys and values in free form style (see the example) |  
| `-o`, `--operation` | The operation to perform | There is no default.  You must specify `read`, `get`, `set`, remove`, or `test` as an argument. | 
|  `-v`, `--verbose`  | Enable verbose debugging | Debugging is not enabled |


#### Arguments

- `key ...` for `get` and `remove` operations
- `key=value...` for `set` operations

If key/value pairs are not specified as arguments on the command line for `set` operations, they are read from stdin.

## Example

### Basic example
Here's a basic example of creating a store and accessing it

```
$ ls $HOME/.private/foo                 # the secure key file does not already exist
ls: cannot access '/home/mrbruno/.private/foo': No such file or directory
$ SecureKeyValues.py -s foo -o set foo=bar
Key for 'foo': 
$ ls $HOME/.private/foo                 # the secure key file was created
/home/mrbruno/.private/foo
$ cat $HOME/.private/foo                # the secure key file is encrypted
gAAAAABcaIw9vBPYKxIiOdKmAONeQ729pOp6JjeTd3KT4tFSs4w2X52rNfyeMUkYZtwH2rRQBDHEXBIfdvw9A2jcyRgEAbywRA==$ 
$ SecureKeyValues.py -s foo -o read     # display entire file in default style
Key for 'foo': 
foo: bar
$ SecureKeyValues.py -s foo -o read -j  # display entire file in json style
Key for 'foo': 
{
  "pairs": {
    "foo": "bar"
  }
}
$ SecureKeyValues.py -s foo -o get foo  # get a specific key from the store
Key for 'foo': 
bar
$ fernet -d < $HOME/.private/foo        # we can decrypt the secure key file ourselves - the key/value pairs are just stored in JSON form
Encryption key: 
{"foo": "bar"}$ 
$ 

```

Note this makes use of my [`fernet`](fernet.md) tool.

### Python example
Here's an example of a Python script that makes use of the class to obtain the value of a secure key.  It's also a great example of using the ssh private key as the encryption key.

```
$ rm -f $HOME/.private/foo
$ SecureKeyValues.py -s foo -o set foo=bar --ssh
$ cat ./keytest
#! /usr/bin/env python
from SecureKeyValues import SecureKeyValues
store = SecureKeyValues('foo', ssh=True)
print store.get('foo')
print store.store
$ ./keytest
bar
{u'foo': u'bar'}
$ 
```

## Notes

- [Fernet encryption](https://cryptography.io/en/latest/fernet) is used to secure the sensitive information.  The Python cryptography package must be installed to use SecureKeyValues.py.  For  instructions on how to install it, see https://pypi.org/project/cryptography/.
- Be careful of your encryption key because I know of no way to recover a key after you've encrypted data and have forgotten the key.  The encryption would probably be worthless if the key could be easily recovered.
- The `--ssh` key was recently added for use with my `mongocli` command and I think it's a no-brainer!  I highly recommend the use of this option!
  - An advantage to **not** using `-ssh` is that the secure store file is portable to any system as long as you know the encryption key.  It is possible that you can use the same secure store file on another system when you encrypt it with `-ssh` but **only if** both systems have the same set of RSA ssh keys.  This is possible but not likely.
