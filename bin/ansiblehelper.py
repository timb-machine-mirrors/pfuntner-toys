#! /usr/bin/env python3

import re
import logging
import argparse

from table import Table

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

class AnsibleHelper(object):

  @staticmethod
  def find_hosts(root):
    """
    Traverse a dictionary/list structure finding hosts
    """
    ret = {}
    if isinstance(root, dict):
      for (name, keys) in root.keys():
        if 'ansible_host' in root[name]:
          ret[name] = keys
        ret.update(AnsibleHelper.find_hosts(keys))
    elif isinstance(root, list):
      for datum in root:
        ret.update(AnsibleHelper.find_hosts(datum))
    return ret

  @staticmethod
  def get_hosts():
    """
    Extracts all hosts from /etc/ansible/hosts files of the following formats:
    
      INI:
        remotehost ansible_user=centos ansible_host=100.101.102.103 ansible_ssh_private_key_file=/home/foo/bar.pem

      Yaml:
        remotehost:
          ansible_user: centos
          ansible_host: 100.101.102.103
          ansible_ssh_private_key_file: /home/foo/bar.pem

    @return: A dictionary of dictionaries.  The top level keys are host and their values contain keys such as
    'ansible_user' and 'ansible_host' having string values
    """

    hosts = {}
    
    with open('/etc/ansible/hosts') as stream:
      data = stream.read()

    try:
      import yaml
      root = yaml.load(data, Loader=yaml.SafeLoader)
    except Exception as e:
      log.debug('Ignoring {e!s} from parsing /etc/ansible/hosts as YAML'.format(**locals()))
    else:
      log.info('Processing /etc/ansible/hosts as YAML')
      hosts = AnsibleHelper.find_hosts(root)

    if not hosts:
      # handle file as INI lines
      name_regexp = re.compile('^(\w\S+)')
      key_regexp = re.compile('(\S+)=(\S+)')
    
      for line in data.splitlines():
        match = name_regexp.search(str(line))
        if match:
          name = match.group(1)
          hosts[name] = {}
          for hit in key_regexp.findall(str(line)):
            hosts[name][hit[0]] = hit[1]
          log.debug('host: {}'.format(hosts))

    return hosts

  @staticmethod
  def get_host(name):
    """
    Extracts host from /etc/ansible/hosts files of the following formats:

      INI:
        remotehost ansible_user=centos ansible_host=100.101.102.103 ansible_ssh_private_key_file=/home/foo/bar.pem

      Yaml:
        remotehost:
          ansible_user: centos
          ansible_host: 100.101.102.103
          ansible_ssh_private_key_file: /home/foo/bar.pem

    @param name: Name of the host as a string
    @return: A dictionary containing keys such as 'ansible_user' and 'ansible_host' having string values
    @raise Exception: Host not found, ansible_user or ansible_host not defined
    """
    hosts = AnsibleHelper.get_hosts()

    if name not in hosts:
      raise Exception('Could not find host {name!r}'.format(**locals()))

    if 'ansible_user' not in hosts[name]:
      raise Exception('Could not find `ansible_user` key in {host}'.format(host=hosts[name]))

    if 'ansible_host' not in hosts[name]:
      raise Exception('Could not find `ansible_host` key in {host}'.format(host=hosts[name]))

    return hosts[name]

  @staticmethod
  def get_host_using_yaml(name, root):
    """
    Extracts host from a dictonary, presumably read from /etc/ansible/hosts.  This could be just a portion of the total dictionary when working recursively.

    @param name: Name of host to extract as a string.
    @param root: The current portion of the dictionary to examine.
    @return: A dictionary from root that matches the host or an empty dictionary if the host is not found.
    """

    ret = {}
    if isinstance(root, dict):
      for (key, value) in root.items():
        if key == name:
          ret = value
        else:
          ret = AnsibleHelper.get_host_using_yaml(name, value)
        if ret:
          break
          
    return ret

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='ssh to ansible target ansible host')

  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-l', '--list', action='store_true', help='List all hosts')
  group.add_argument('host', nargs='?', help='The name of the target host')

  parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Enable ssh quiet mode')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  args = parser.parse_args()
  log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  if args.list:
    table = Table(['host', 'user', 'ip'])
    for (name, keys) in AnsibleHelper.get_hosts().items():
      table.add(name, keys.get('ansible_host', ''), keys.get('ansible_user', ''))
    print(str(table))
  else:
    print(AnsibleHelper.get_host(args.host))
