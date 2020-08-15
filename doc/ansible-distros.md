# `ansible-distros`

## Purpose
Show information about various hosts, relying on Ansible and `ssh`

## Syntax
```
Syntax: ansible-distros [-i INVENTORY] [-n] [nodes [nodes ...]]
```

### Options and arguments

`nodes` is zero or more host names and defaults to the Ansible `all` concept.

| Option | Description | Default |
| ------ | ----------- | ------- |
| `-i INVENTORY`, `--inventory INVENTORY` | Path to Ansible inventory YAML file. | Use the default Ansible locations |
| `-n`, `--names` | Retain actual Ansible names that you might use as a variable name in an Ansible script. | Friendly column names are typically used.  See the note below for the actual names |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Examples
I have several AWS Cloud instances running and set up Ansible to use them via `/etc/ansible/hosts`:

```
$ ansible-distros
Node           OS Family  Distro  Version  Major Version  Distro Release  Kernel                         Package Manager  Service Manager
bruno-amazon1  RedHat     Amazon  2018.03  NA             NA              4.14.186-110.268.amzn1.x86_64  yum              upstart
bruno-amazon2  RedHat     Amazon  (Karoo)  NA             NA              4.14.177-139.254.amzn2.x86_64  yum              systemd
bruno-rh8      RedHat     RedHat  8.2      8              Ootpa           4.18.0-193.el8.x86_64          dnf              systemd
$
```

Here's how it looks when you use the actual Ansible names for the column headings:
```
$ ansible-distros -n
Node           ansible_os_family  ansible_distribution  ansible_distribution_version  ansible_distribution_major_version  ansible_distribution_release  ansible_kernel                 ansible_pkg_mgr  ansible_service_mgr
bruno-amazon1  RedHat             Amazon                2018.03                       NA                                  NA                            4.14.186-110.268.amzn1.x86_64  yum              upstart
bruno-amazon2  RedHat             Amazon                (Karoo)                       NA                                  NA                            4.14.177-139.254.amzn2.x86_64  yum              systemd
bruno-rh8      RedHat             RedHat                8.2                           8                                   Ootpa                         4.18.0-193.el8.x86_64          dnf              systemd
$
```

#### localhost
Personally, I don't usually have `localhost` in my `/etc/ansible/hosts` but Ansible often works for `localhost`.
```
$ ansible-distros localhost
Node       OS Family  Distro  Version  Major Version  Distro Release  Kernel              Package Manager  Service Manager
localhost  Debian     Ubuntu  18.04    18             bionic          5.3.0-7648-generic  apt              systemd
$ 
```

## Notes

- The tool depends heavily on Ansible and uses `ansible host -m setup` to gather the information it displays.  I developed it in a job where I was making heavy use of cloud machines and Ansible to configure the machines.
- The mappings between _friendly_ and _actual_ names for columns is:

    | Friendly name | Actual name |
    | ----- | ------ |
    | OS Family | ansible_os_family |
    | Distro | ansible_distribution |
    | Version | ansible_distribution_version |
    | Major Version | ansible_distribution_major_version |
    | Distro Release | ansible_distribution_release |
    | Kernel | ansible_kernel |
    | Package Manager | ansible_pkg_mgr |
    | Service Manager | ansible_service_mgr |
