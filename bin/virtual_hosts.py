#! /usr/bin/env python

import os
import re
import json
import logging
import argparse
import datetime
import subprocess

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

class Host(object):
  required_keys = set(['name', 'ip', 'user'])

  def __init__(self, src, **kwargs):
    missing_keys = Host.required_keys - set(kwargs.keys())
    if missing_keys:
      log.error('{kwargs} is missing {missing_keys}'.format(expected=list(Host.required_keys), **locals()))
      exit(1)
    for (key, value) in kwargs.items():
      setattr(self, key, value)
    self.src = src
    log.debug('Created {self!s} from {kwargs}'.format(**locals()))

  def __str__(self):
    remains = set(dir(self)) - Host.required_keys
    elements = [
      'name: {self.name}'.format(**locals()),
      'ip: {self.ip}'.format(**locals()),
      'user: {self.user}'.format(**locals()),
    ]
    for key in sorted(remains):
      value = getattr(self, key)
      if isinstance(value, basestring) and (not key.startswith('__')):
        elements.append('{key}: {value}'.format(**locals()))
    return ', '.join(elements)

class VirtualHosts(object):

  ANSIBLE_HOSTS_FILE = '/etc/ansible/hosts'
  AWS_CREDS_FILE = '{HOME}/.aws/credentials'.format(**os.environ)

  int_regexp = re.compile('^\d+$')

  def __init__(self, **kwargs):
    self.profile = kwargs.get('profile')
    self.get_images = kwargs.get('get_images')
    self.ansible_only = kwargs.get('ansible_only')
    self.aws_only = kwargs.get('aws_only')
    self.shallow = kwargs.get('shallow')

    self.aws_instance_cache = {}
    self.aws_image_cache = {}
    self.warnings = [] # lists use 4.25x less storage than sets

  @classmethod
  def find_nodes(cls, root, required_key):
    ret = []
    if isinstance(root, list):
      for node in root:
        ret += cls.find_nodes(node, required_key)
    elif isinstance(root, dict):
      for (key, node) in root.items():
        if isinstance(node, dict) and required_key in node.keys():
          node['name'] = key
          ret.append(node)
        ret += cls.find_nodes(node, required_key)
    return ret

  def get_ansible_hosts(self):
    ret = []
    if os.path.isfile(self.ANSIBLE_HOSTS_FILE):
      with open(self.ANSIBLE_HOSTS_FILE) as stream:
        data = stream.read()

      try:
        import yaml
        root = yaml.load(data, Loader=yaml.SafeLoader)
      except Exception as e:
        log.debug('Ignoring {e!s} from parsing {self.ANSIBLE_HOSTS_FILE} as YAML'.format(**locals()))
      else:
        # process the YAML nodes
        nodes = self.find_nodes(root, 'ansible_host')
        log.debug('YAML nodes: {nodes}'.format(**locals()))
        for node in nodes:
          attrs = {
            'name': node['name'],
            'ip':   node['ansible_host'],
            'user': node['ansible_user'],
          }
          if 'ansible_ssh_private_key_file' in node:
            attrs['key'] = node['ansible_ssh_private_key_file']
          ret.append(Host('yaml', **attrs))

      if not ret:
        log.debug('Processing {self.ANSIBLE_HOSTS_FILE} as an INI file'.format(**locals()))
        name_regexp = re.compile(r'^(\w\S+)')
        key_regexp = re.compile(r'(\S+)=(\S+)')

        for line in data.splitlines():
          match = name_regexp.search(line)
          if match:
            attrs = {
              'name': match.group(1),
            }
            for hit in key_regexp.findall(line):
              key = hit[0]
              value = hit[1]
              if key == 'ansible_host':
                key = 'ip'
              elif key == 'ansible_user':
                key = 'user'
              elif key == 'ansible_ssh_private_key_file':
                key = 'key'
              attrs[key] = value
            ret.append(Host('ini', **attrs))
    else:
      log.debug('No {self.ANSIBLE_HOSTS_FILE} file'.format(**locals()))

    log.debug('ansible hosts: {}'.format([str(host) for host in ret]))
    return ret

  @classmethod
  def get_value(cls, root, path):
    if not root:
      return root

    if not path:
      return root or None

    if isinstance(path, basestring):
      path = path.split('/')

    if cls.int_regexp.search(path[0]) and isinstance(root, list):
      pos = int(path[0])
      if 0 <= pos < len(root):
        return cls.get_value(root[pos], path[1:])
      else:
        return None
    else:
      return cls.get_value(root.get(path[0], {}), path[1:])

  def get_user(self, image_name):
    ret = None
    if image_name:
      image_name = image_name.lower()
      if 'amazon linux' in image_name:
        ret = 'ec2-user'
      elif 'ubuntu' in image_name:
        ret = 'ubuntu'
      elif 'debian' in image_name:
        ret = 'admin'
      elif 'red hat' in image_name:
        ret = 'ec2-user'
      elif 'centos' in image_name:
        ret = 'centos'
      else:
        log.info('Could not determine user from image description {image_name!r}'.format(**locals()))

    return ret

  def get_image(self, image_id):
    ret = None
    if image_id:
      image = self.aws_image_cache.get(image_id)
      if image:
        log.info('Using cached image')
      else:
        # get the image from the aws cli
        cmd = ['aws' ,'ec2']
        if self.profile:
          cmd += ['--profile', self.profile]
        cmd += ['describe-images', '--image-ids', image_id]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        rc = p.wait()
        log.debug('{cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
        if (rc == 0) and (not stderr):
          try:
            images = json.loads(stdout)
          except Exception as e:
            log.info('Could not parse aws cli output: {e!s}'.format(**locals()))
          else:
            ret = self.get_value(images, 'Images/0')
            self.aws_image_cache[image_id] = ret # cache this image for future use
    return ret

  def make_elapsed(self, attrs, name):
    # '2019-09-04T13:35:58.000Z'
    attrs[name + '_elapsed'] = None
    if attrs.get(name):
      try:
        ts = datetime.datetime.strptime(attrs.get(name)[:-1], '%Y-%m-%dT%H:%M:%S.%f')
      except Exception as e:
        log.debug('{e!s} parsing {value}'.format(value=attrs.get(name), **locals()))
      else:
        attrs[name + '_elapsed'] = str(datetime.datetime.utcnow() - ts)

  def get_aws_hosts(self):
    ret = []
    key_template = '{HOME}/.ssh/{{key_name}}.pem'.format(**os.environ)

    if os.path.isfile(self.AWS_CREDS_FILE):
      cmd = ['aws', 'ec2']
      if self.profile:
        cmd += ['--profile', self.profile]
      cmd += ['describe-instances']
      try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      except Exception as e:
        log.debug('Caught {e!s} executing {cmd}'.format(**locals()))
      else:
        (stdout, stderr) = p.communicate()
        rc = p.wait()
        log.debug('{cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
        if (rc == 0) and (not stderr):
          try:
            resp = json.loads(stdout)
          except Exception as e:
            log.info('Could not parse aws cli output')
          else:
            """
            /BlockDeviceMappings/0/Ebs/AttachTime '2019-09-04T13:35:58.000Z'
            /LaunchTime '2019-09-07T02:43:57.000Z'
            /NetworkInterfaces/0/Attachment/AttachTime '2019-09-04T13:35:57.000Z'
            """
            for instance in resp.get('Reservations', []):
              instance_id = self.get_value(instance, 'Instances/0/InstanceId')
              self.aws_instance_cache[instance_id] = self.get_value(instance, 'Instances/0')
              state = self.get_value(instance, 'Instances/0/State/Name')
              attrs = {
                'instance_id': instance_id,
                'name': self.get_value(instance, 'Instances/0/Tags/0/Value'),
                'ip': self.get_value(instance, 'Instances/0/PublicIpAddress') if state == 'running' else None,
                'user': None,
                'zone': self.get_value(instance, 'Instances/0/Placement/AvailabilityZone'),
                'created': self.get_value(instance, 'Instances/0/NetworkInterfaces/0/Attachment/AttachTime'),
                'controlled': self.get_value(instance, 'Instances/0/LaunchTime'),
                'state': state,
                'image_id': self.get_value(instance, 'Instances/0/ImageId'),
                'image_name': None,
              }
              self.make_elapsed(attrs, 'created')
              self.make_elapsed(attrs, 'controlled')

              key_name = self.get_value(instance, 'Instances/0/KeyName')
              if key_name:
                key_path = key_template.format(**locals())
                if os.path.isfile(key_path):
                  attrs['key'] = key_path
                else:
                  log.info('Can\'t find key {key_name!r}'.format(**locals()))
              else:
                log.warning('No key for {name}'.format(name=attrs['name']))

              ret.append(Host('aws', **attrs))
    else:
      log.debug('No {self.AWS_CREDS_FILE} file'.format(**locals()))

    log.debug('aws hosts: {}'.format([str(host) for host in ret]))
    return ret

  def get_hosts(self, *names):

    ret = {}

    if (len(names) == 1) and isinstance(names[0], list):
      names = names[0] or ['.']

    ansible_hosts = [] if self.aws_only else self.get_ansible_hosts()
    aws_hosts = None
    for name in names:
      curr = []
      exact = False
      for host in ansible_hosts:
        if name == host.name:
          curr.append(host)
          exact = True
          break
        elif re.search(name, host.name):
          curr.append(host)

      if (not curr) or (not exact):
        if aws_hosts is None:
          aws_hosts = [] if self.ansible_only else self.get_aws_hosts()
        for host in aws_hosts:
          log.debug('Comparing {host.name} against {name}'.format(**locals()))
          if name == host.name:
            curr.append(host)
            break
          else:
            try:
              match = re.search(name, host.name)
              log.debug('Regexp: {}'.format(bool(match)))
            except Exception as e:
              if name not in self.warnings:
                log.warning('{name!r} has not a valid regular expression: {e!s}'.format(**locals()))
                self.warnings.append(name)
            else:
              if match:
                curr.append(host)

      if not curr:
        log.warning('No match for {name!r}'.format(**locals()))
      else:
        for host in curr:
          if host.name not in ret.keys():
            ret[host.name] = host

    for host in ret.values():
      if host.src == 'aws':
        self.aws_image_cache[host.image_id] = None

    log.info('There are {count} AWS images that need to be examined to find the userid'.format(count=len(self.aws_image_cache)))
    if (not self.shallow) and ((0 < len(self.aws_image_cache) <= 2) or self.get_images):
      # complete aws users by looking at the images on which the instances are based
      for host in ret.values():
        if (host.user is None) and (host.src == 'aws') and (hasattr(host, 'image_id')):
          image = self.get_image(host.image_id)
          host.image_name = self.get_value(image, 'Description')
          host.user = self.get_user(host.image_name)

    ret = sorted([host for host in ret.values()], key=lambda host: host.name)
    log.debug('get_hosts({names}) returning {hosts}'.format(hosts=[str(host) for host in ret], **locals()))

    return ret

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Virtual Host Helper')
  parser.add_argument('-p', '--profile', dest='profile', help='Specify AWS configuration profile')
  parser.add_argument('--get-images', action='store_true', help='Get all AWS images for user resolution (slow)')
  parser.add_argument('--aws-only', action='store_true', help='Ignore Ansible hosts file - use AWS CLI only')
  parser.add_argument('-v', '--verbose', dest='verbose', action='count', help='Enable debugging')
  parser.add_argument('hostnames', metavar='hostname', nargs='*', help='Zero or more host names')
  args = parser.parse_args()

  log.setLevel(logging.WARNING - 10*(args.verbose or 0))

  virtual_hosts = VirtualHosts(**args.__dict__)

  hosts = virtual_hosts.get_hosts(args.hostnames)
  for host in hosts:
    print host
