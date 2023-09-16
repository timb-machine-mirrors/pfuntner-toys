# `push-ssh-key`

## Purpose
Push your public ssh key to a remote system's `authorized_keys` file to enable passwordless-ssh.

## Syntax
```
Syntax: push-ssh-key [-h] [--dry-run] [-v] remote [public-key]
```
### Positional arguments
- `remote`: ssh target

    Examples:
    - `hostname`
    - `ip`
    - `user@hostname`
    - `user@ip`
- `public-key-path`: Path to public key to push
 
    Defaults to:
    - First choice: `~/.ssh/id_rsa.pub` 
    - Second choice if `~/.ssh/id_rsa.pub` is not found: `~/.ssh/id_dsa.pub` 

### Options
| Option      | Description                                                                                                                            | Default                  |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| `--dry-run` | Do not push the public key, only display command that would have been used                                                             | Public key is pushed     |
| `-v`        | Enable verbose debugging<br>`-v`: public key and its path are printed<br>`-vv`: Same as `-v` but command to add the key is printed too | Debugging is not enabled |

## Examples

<img alt="Under Construction" height="133" src="images/under-construction.jpg" title="Coming Soon" width="200"/>
<br><a href="https://www.freepik.com/free-vector/coming-soon-construction-yellow-background-design_8562867.htm#query=work%20in%20progress&position=49&from_view=keyword&track=ais">Image by starline</a> on Freepik

```
# Coming soon to a markdown page near you!
```

## Notes

- `ssh` is used under the covers but since password-less ssh is likely not enabled, your password will be prompted for
- Not only is the public key appended to `~/.ssh/authorized_keys` but the script also ensures the permissions of `~/.ssh/authorized_keys` are `0600` - `ssh` can be super-picky about that so I think it's a good precaution, especially if the script _creates_ `~/.ssh/authorized_keys`!
- If you don't have a public ssh key to push, remember that you can use [`ssh-keygen`](https://man7.org/linux/man-pages/man1/ssh-keygen.1.html) to create one.  I know the prompts can seem a little confusing - I always just accept all of the defaults!
- The public key is just appended to the end of `~/.ssh/authorized_keys` on the remote target.  If you run the script twice to the same system, it will add two copies of the key.  It might make sense to do something to check to see if the key is already present.
