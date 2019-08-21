#! /usr/bin/env python

import re
import logging
import argparse

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

class AnsibleHelper(object):

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
    @param depth: Recursion depth, typically entered defaulted to 0 caller.  This is used for Yaml processing to know when we've processed everything
    @return: A dictionary containing keys such as 'ansible_user' and 'ansible_host' having string values
    @raise Exception: Host not found, ansible_user or ansible_host not defined
    """

    ret = {}
    
    with open('/etc/ansible/hosts') as stream:
      data = stream.read()

    try:
      import yaml
      root = yaml.load(data, Loader=yaml.SafeLoader)
    except Exception as e:
      log.debug('Ignoring {e!s} from parsing /etc/ansible/hosts as YAML'.format(**locals()))
    else:
      log.info('Processing /etc/ansible/hosts as YAML')
      ret = AnsibleHelper.get_host_using_yaml(name, root)

    if not ret:
      # handle file as INI lines
      regexp = re.compile('(\S+)=(\S+)')
    
      for line in data.splitlines():
        tokens = line.split()
        if tokens and (tokens[0] == name):
          for hit in regexp.findall(line):
            log.debug('ret: {ret}, hit: {hit}'.format(**locals()))
            ret[hit[0]] = hit[1]
          break
    
    if not ret:
      raise Exception('Could not find host {name!r}'.format(**locals()))

    if 'ansible_user' not in ret:
      raise Exception('Could not find `ansible_user` key in {ret}'.format(**locals()))

    if 'ansible_host' not in ret:
      raise Exception('Could not find `ansible_host` key in {ret}'.format(**locals()))

    return ret

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
  parser.add_argument('host', help='The name of the target host')
  parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Enable ssh quiet mode')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
  args = parser.parse_args()
  log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

  print AnsibleHelper.get_host(args.host)
