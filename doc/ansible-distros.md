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
#### Ansible setup
I have several AWS Cloud instances running and set up Ansible to use them via `/etc/ansible/hosts`:

```
$ cat /etc/ansible/hosts
[targets]
bruno-amazon1 ansible_host=3.83.98.175 ansible_user=ec2-user ansible_ssh_private_key_file=/home/mrbruno/.ssh/bruno.pem
bruno-amazon2 ansible_host=100.25.192.145 ansible_user=ec2-user ansible_ssh_private_key_file=/home/mrbruno/.ssh/bruno.pem
bruno-rh8 ansible_host=100.26.227.68 ansible_user=ec2-user ansible_ssh_private_key_file=/home/mrbruno/.ssh/bruno.pem
$
```
I actually have another tool that can generate this file along with `~/.ssh/config` for cloud machines from _Amazon Web Services_ (AWS) or _Google Cloud Platform_ (GCP) but I'm not sure how universal the tool is.  I would love for someone to try it out so let me know if you're interested.

### Basic example
```
$ ansible-distros
Node           OS Family  Distro  Version  Major Version  Distro Release  Kernel                         Package Manager  Service Manager
bruno-amazon1  RedHat     Amazon  2018.03  NA             NA              4.14.186-110.268.amzn1.x86_64  yum              upstart
bruno-amazon2  RedHat     Amazon  (Karoo)  NA             NA              4.14.177-139.254.amzn2.x86_64  yum              systemd
bruno-rh8      RedHat     RedHat  8.2      8              Ootpa           4.18.0-193.el8.x86_64          dnf              systemd
$
```

### Actual Ansible names
Here's how it looks when you use the actual Ansible names for the column headings:
```
$ ansible-distros -n
Node           ansible_os_family  ansible_distribution  ansible_distribution_version  ansible_distribution_major_version  ansible_distribution_release  ansible_kernel                 ansible_pkg_mgr  ansible_service_mgr
bruno-amazon1  RedHat             Amazon                2018.03                       NA                                  NA                            4.14.186-110.268.amzn1.x86_64  yum              upstart
bruno-amazon2  RedHat             Amazon                (Karoo)                       NA                                  NA                            4.14.177-139.254.amzn2.x86_64  yum              systemd
bruno-rh8      RedHat             RedHat                8.2                           8                                   Ootpa                         4.18.0-193.el8.x86_64          dnf              systemd
$
```
And here's how to make use of those awesome variables:
```
$ cat distros.yml
- name: Example of using Ansible builtin variables
  hosts: all
  tasks:
  - debug:
      msg: "I am {{ansible_distribution}} {{ansible_distribution_version}}"
$ ansible-playbook distros.yml

PLAY [Example of using Ansible builtin variables] ************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************
ok: [bruno-amazon2]
ok: [bruno-amazon1]
ok: [bruno-rh8]

TASK [debug] *************************************************************************************************************************************************************
ok: [bruno-amazon1] => {
    "msg": "I am Amazon 2018.03"
}
ok: [bruno-amazon2] => {
    "msg": "I am Amazon (Karoo)"
}
ok: [bruno-rh8] => {
    "msg": "I am RedHat 8.2"
}

PLAY RECAP ***************************************************************************************************************************************************************
bruno-amazon1              : ok=2    changed=0    unreachable=0    failed=0
bruno-amazon2              : ok=2    changed=0    unreachable=0    failed=0
bruno-rh8                  : ok=2    changed=0    unreachable=0    failed=0

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

- The tool depends heavily on Ansible and uses `ansible host -m setup` to gather the information it displays.  Seriously, the Ansible `setup` module is freaking AWESOME!  I developed my tool in a job where I was making heavy use of cloud machines and Ansible to configure the machines.
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
