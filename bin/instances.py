#! /usr/bin/env python3
import os
import re
import sys
import json
import getpass
import inspect
import logging
import argparse
import subprocess

class Instance(object):
  def __init__(self, provider, true_name, name, id, image_id, image_name, distro, user, ip, key_filename, active):
    self.provider = provider
    self.true_name = true_name
    self.name = name
    self.id = id
    self.image_id = image_id
    self.image_name = image_name
    self.distro = distro
    self.user = user
    self.ip = ip
    self.key_filename = key_filename
    self.active = bool(active)

  def __str__(self):
    return json.dumps(self.__dict__)

class Instances(object):
  def __init__(self, log):
    self.log = log

    self.ssh_root = os.path.expandvars("$HOME/.ssh")
    self.ssh_config_filename = os.path.join(self.ssh_root, 'config')

    basename = os.path.basename(inspect.getfile(self.__class__))
    if basename.endswith('.py'):
      basename = basename[:-3]
    self.config_name = os.path.join(os.environ['HOME'], basename + '.json')
    self.log.debug(f'config_name={self.config_name!r}')
    if os.path.isfile(self.config_name):
      with open(self.config_name) as stream:
        try:
          self.config = json.load(stream)
        except Exception as e:
          raise Exception(f'Could not parse {self.config_name!r}: "{e!s}"')
        self.log.debug(f'config: {self.config}')
    else:
      self.log.warn(f'Could not find config {self.config_name!r}')
      self.config = {}

    if 'gcp_user' not in self.config:
      self.config['gcp_user'] = getpass.getuser()
      self.log.info('Assuming gcp_user={}'.format(self.config['gcp_user']))

  def backfill_aws_image_info(self, instances):
    aws_distro_mappings = [
      (re.compile('ubuntu-?[a-z]*-16'),  'ubuntu16', 'ubuntu'),
      (re.compile('ubuntu-?[a-z]*-18'),  'ubuntu18', 'ubuntu'),
      (re.compile('^CentOS[ A-Za-z]+6'), 'centos6',  'centos'),
      (re.compile('^CentOS[ A-Za-z]+7'), 'centos7',  'centos'),
      (re.compile('^CentOS[ A-Za-z]+8'), 'centos8',  'centos'),
      (re.compile('^debian-jessie'),     'debian8',  'admin'),
      (re.compile('^debian-stretch'),    'debian9',  'admin'),
      (re.compile('^debian-10'),         'debian10', 'admin'),
      (re.compile('^amzn-'),             'amazon1',  'ec2-user'),
      (re.compile('^amzn2'),             'amazon2',  'ec2-user'),
      (re.compile('^RHEL-6'),            'rhel6',    'ec2-user'),
      (re.compile('^RHEL-7'),            'rhel7',    'ec2-user'),
      (re.compile('^RHEL-8'),            'rhel8',    'ec2-user'),
    ]

    image_ids = list(set([instance.image_id for instance in instances if instance.provider == 'aws']))
    self.log.debug(f'image_ids to query: {image_ids}')
    if image_ids:
      (rc, stdout, stderr) = self.run(['aws', 'ec2', 'describe-images', '--image-ids'] + image_ids)
      if rc == 0 and stdout:
        raw = json.loads(stdout).get('Images', [])
        for image in raw:
          image_id = image.get('ImageId')
          image_name = image.get('Name')
          if image_name:
            distro = None
            user = None

            for mapping in aws_distro_mappings:
              if mapping[0].search(image_name):
                distro = mapping[1]
                user = mapping[2]
                break

            log.debug(f'image: {image_id} {image_name} {distro} {user}')

            if distro and user:
              for instance in instances:
                if instance.image_id == image_id:
                  log.debug(f'Updating image info for {instance.name}')
                  instance.image_name = image_name
                  instance.distro = distro
                  instance.user = user
            else:
              raise Exception(f'No distro or user for {image_id}')
          else:
            raise Exception(f'No name found for {image_id}')

    remaining_instances = [instance for instance in instances if instance.provider == 'aws' and not (instance.image_name and instance.distro and instance.user)]
    if remaining_instances:
      raise Exception(f'Some AWS instances have incomplete image information: {remaining_instances}')

  def backfill_gcp_image_info(self, instances):
    gcp_distro_mappings = [
      (re.compile('^centos-7'),          'centos7'),
      (re.compile('^centos-8'),          'centos8'),
      (re.compile('^rhel-7'),            'rhel7'),
      (re.compile('^rhel-8'),            'rhel8'),
      (re.compile('^debian-9'),          'debian9'),
      (re.compile('^debian-10'),         'debian10'),
      (re.compile('^ubuntu[-a-z]*-16'),  'ubuntu16'),
      (re.compile('^ubuntu[-a-z]*-18'),  'ubuntu18'),
    ]

    user = self.config.get('gcp_user')

    image_ids = list(set([instance.image_id for instance in instances if instance.provider == 'gcp']))
    self.log.debug(f'image_ids to query: {image_ids}')
    if image_ids:
      (rc, stdout, stderr) = self.run(['gcloud', '--format', 'json', 'compute', 'disks', 'list', '--filter', 'name:(' + ' '.join(image_ids) + ')'])
      if rc == 0 and stdout:
        for image in json.loads(stdout):
          self.log.debug(f'Now processing: {image}')
          distro = None

          """
          There's an `id` field (a long unique integer) that I at first tried to
          use but it's not available from `gcloud compute instances list`.  The
          `name` field is better to use in this instance.
          """
          image_id = image.get('name')

          image_name = os.path.basename(image.get('sourceImage'))
          for regexp, mapping in gcp_distro_mappings:
            if regexp.search(image_name):
              distro = mapping
              break

          self.log.debug(f'image: {image_id!r} {image_name!r} {distro!r} {user!r}')
          if distro and user:
            for instance in instances:
              if instance.image_id == image_id:
                self.log.debug(f'Updating image info for {instance.name}')
                instance.image_name = image_name
                instance.distro = distro
                instance.user = user
          else:
            raise Exception(f'No distro or user for {image_id}')

    remaining_instances = [instance for instance in instances if instance.provider == 'gcp' and not (instance.image_name and instance.distro and instance.user)]
    if remaining_instances:
      raise Exception(f'Some GCP instances have incomplete image information: {remaining_instances}')

  def run(self, cmd):
    if isinstance(cmd, str):
      cmd = cmd.split()
    rc = None
    stdout = None
    stderr = None
    self.log.info('Executing {cmd}'.format(**locals()))
    try:
      p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
      log.info(f'Caught: {e!s}')
    else:
      (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
      rc = p.wait()

    self.log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
    return (rc, stdout, stderr)

  def extract(self, root, path):
    if isinstance(path, str):
      path = path.split('/')
    key = path.pop(0)
    if isinstance(root, list):
      if key.isdecimal():
        key = int(key)
        if key < len(root):
          root = root[key]
        else:
          root = None
      else:
        root = None
    elif isinstance(root, dict):
      root = root.get(key)
    
    if root and path:
      return self.extract(root, path)
    else:
      return root

  def get_instances(self):
    name_regexp = re.compile(self.config.get('regexp', '.'))
    remove_regexp = bool(self.config.get('remove_regexp', 'false'))

    instances = []

    provider = 'aws'
    (rc, stdout, stderr) = self.run('aws ec2 describe-instances')
    if rc == 0 and stdout:
      raw = json.loads(stdout)
      for raw_reservation in raw.get('Reservations', []):
        for instance in raw_reservation.get('Instances', []):
          id = instance.get('InstanceId')

          true_name = None
          name = None
          image_id = None
          image_name = None
          distro = None
          user = None
          ip = self.extract(instance, 'NetworkInterfaces/0/Association/PublicIp')
          key_name = instance.get('KeyName')
          key_filename = os.path.join(self.ssh_root, key_name + '.pem') if key_name else None
          active = self.extract(instance, 'State/Name') == 'running'

          if not id:
            raise Exception(f'No instance ID in {instance}')
          self.log.info(f'aws instance id: {id}')
          name = None
          for tag in instance.get('Tags', []):
            self.log.debug(f'Examing tag {tag}')
            if tag.get('Key') == 'Name':
              name = tag.get('Value')
              break
          if name:
            self.log.info(f'instance name: {name}')
            match = name_regexp.search(name)
            if match:
              true_name = name
              self.log.debug(f'instance {name} is desired')
              if remove_regexp:
                name = name[:match.start(0)] + name[match.end(0):]
                self.log.debug(f'after removing regular expression, instance name is {name}')

              image_id = instance.get('ImageId')
              self.log.debug(f'Instance {name} ({id}) uses image {image_id}')

              instances.append(Instance(provider, true_name, name, id, image_id, image_name, distro, user, ip, key_filename, active))
          else:
            self.log.debug(f'No name for instance {id}')

    self.backfill_aws_image_info(instances)

    provider = 'gcp'
    key_filename = os.path.join(self.ssh_root, 'google_compute_engine')
    (rc, stdout, stderr) = self.run('gcloud --format json compute instances list')
    if rc == 0 and stdout:
      raw = json.loads(stdout)
      for instance in raw:
        id = instance.get('id')

        image_id = None
        image_name = None
        distro = None
        user = None
        ip = self.extract(instance, 'networkInterfaces/0/accessConfigs/0/natIP')
        active = instance.get('status') == 'RUNNING'

        self.log.info(f'gcp instance id: {id}')
        name = instance.get('name', '')
        match = name_regexp.search(name)
        if match:
          true_name = name
          self.log.debug(f'instance {name} is desired')
          if remove_regexp:
            name = name[:match.start(0)] + name[match.end(0):]
            self.log.debug(f'after removing regular expression, instance name is {name}')
          disks = instance.get('disks', [])
          if disks:
            instances.append(Instance(provider, true_name, name, id, disks[0].get('deviceName'), image_name, distro, user, ip, key_filename, active))
          else:
            self.log.info(f'No device name for {id}/{name}')

    self.backfill_gcp_image_info(instances)

    # add "constant" instances
    for instance in self.config.get('instances', []):
      instances.append(Instance(**instance))

    self.log.debug('instances: {}'.format([instance.__dict__ for instance in instances]))
    return sorted(instances, key=lambda instance: instance.name)

if __name__ == '__main__':
  log = logging.getLogger()
  logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
  log.setLevel(logging.WARNING)

  instances_class = Instances(log)

  parser = argparse.ArgumentParser(description='Discover AWS/GCP instances')
  parser.add_argument('-m', '--make', action='count', help=f'Refresh /etc/ansible/hosts and {instances_class.ssh_config_filename} with instance information')
  parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
  args = parser.parse_args()

  log.setLevel(logging.WARNING - (args.verbose or 0)*10)

  instances = instances_class.get_instances()
  if instances:
    from table import Table
    table = Table('Name', 'Distro', 'User', 'IP', 'Key name')
    for instance in instances:
      table.add(instance.name, instance.distro, instance.user, instance.ip, instance.key_filename)
    print(str(table), end='')

    if args.make:
        print('Writing to /etc/ansible/hosts')
        p = subprocess.Popen(([] if 'win' in sys.platform else ['sudo']) + ['bash', '-c', 'cat > /etc/ansible/hosts'], stdin=subprocess.PIPE)
        p.stdin.write('[targets]\n'.encode())
        for instance in instances:
          p.stdin.write(f'{instance.name} ansible_host={instance.ip} ansible_user={instance.user} ansible_ssh_private_key_file={instance.key_filename}\n'.encode())
        p.stdin.close()
        rc = p.wait()

        print(f'Writing to {instances_class.ssh_config_filename}')
        with open(instances_class.ssh_config_filename, 'w') as stream:
          for instance in instances:
            stream.write(f'Host {instance.name}\n\tHostname {instance.ip}\n\tUser {instance.user}\n\tIdentityFile {instance.key_filename}\n')
        
        subprocess.Popen(['add-to-knownhosts'] + [instance.name for instance in instances]).wait()
  else:
    print('No instances!')
