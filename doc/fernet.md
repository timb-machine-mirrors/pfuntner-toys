# `fernet`

## Purpose
Perform [fernet](https://cryptography.io/en/latest/fernet) encryption/decryption.

## Syntax
```
Syntax: fernet [-v|--verbose] [-d|--decrypt]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |
|  `-d`  | Enable fernet decryption | Fernet encryption is performed |

## Example

```
$ date | fernet | tee /tmp/secret
Encryption key: 
gAAAAABcaH8gaUJzCzoOprHr3RxuNnQo9Utqc9bA4UiU3SiBm0MaPdxmYqpDXOUr_KY0yIJ-kBRQ78NmEo2qdWZNiYd4C1HX4bsGzjQX0lMD4nVy7pzRjNM=$ 
$ fernet -d < /tmp/secret
Encryption key: 
Sat Feb 16 16:22:37 EST 2019
$ 
```

## Notes

- The data must be supplied via stdin.
- Regarding the example:
  - The encryption key is requested for both encryption and decryption.  The characters are **not** echoed to the terminal.
    - I tried to do an example with a single pipeline the encrypted and decrypted the data like so:

      ```
      $ data | encrypt | decrypt -d
      ```

    but did not give this as the primary example because it demonstrates a flaw in not echo'ing the encryption key. Since both the encryption and decryption commands were essentially running at the same time, both blocked reading stdin, as soon as I entered the key the first time, the terminal had reset its echo mode and the second time the encryption key was entered, it appeared on the screen as I typed it.  So be aware of using encryption and decryption in a pipeline like this.
  - The seemingly-random string of bytes is the _encrypted version_ of the data.  The dollar sign at the end of the line is actually **not** part of the encrypted data.  There is no trailing dollar sign in the encrypted file and the dollar sign and what you see is the **shell prompt** showing that the shell is waiting for you to enter your next command.
  - Be careful of your encryption key because I know of no way to recover a key after you've encrypted data and have forgotten the key.  The encryption would probably be worthless if the key could be easily recovered.
