#! /usr/bin/env python3

import os
import re
import sys
import json
import getpass
import logging
import argparse
import subprocess

class Instance(object):
  def __init__(self, provider, name, id, image_id, image_name, distro, user, ip, active):
    self.provider = provider
    self.name = name
    self.id = id
    self.image_id = image_id
    self.image_name = image_name
    self.distro = distro
    self.user = user
    self.ip = ip
    self.active = bool(active)

  def __str__(self):
    return json.dumps(self.__dict__)

def backfill_aws_image_info(instances):

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
  log.debug(f'image_ids to query: {image_ids}')
  if image_ids:
    (rc, stdout, stderr) = run(['aws', 'ec2', 'describe-images', '--image-ids'] + image_ids)
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
            parser.error(f'No distro or user for {image_id}')
        else:
          parser.error(f'No name found for {image_id}')

  remaining_instances = [instance for instance in instances if instance.provider == 'aws' and not (instance.image_name and instance.distro and instance.user)]
  if remaining_instances:
    parser.error(f'Some AWS instances have incomplete image information: {remaining_instances}')

def backfill_gcp_image_info(instances):

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

  user = config.get('gcp_user')

  image_ids = list(set([instance.image_id for instance in instances if instance.provider == 'gcp']))
  log.debug(f'image_ids to query: {image_ids}')
  if image_ids:
    (rc, stdout, stderr) = run(['gcloud', '--format', 'json', 'compute', 'disks', 'list', '--filter', 'name:(' + ' '.join(image_ids) + ')'])
    if rc == 0 and stdout:
      for image in json.loads(stdout):
        log.debug(f'Now processing: {image}')
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

        log.debug(f'image: {image_id!r} {image_name!r} {distro!r} {user!r}')
        if distro and user:
          for instance in instances:
            if instance.image_id == image_id:
              log.debug(f'Updating image info for {instance.name}')
              instance.image_name = image_name
              instance.distro = distro
              instance.user = user
        else:
          parser.error(f'No distro or user for {image_id}')

  remaining_instances = [instance for instance in instances if instance.provider == 'gcp' and not (instance.image_name and instance.distro and instance.user)]
  if remaining_instances:
    parser.error(f'Some GCP instances have incomplete image information: {remaining_instances}')

def run(cmd):
  if isinstance(cmd, str):
    cmd = cmd.split()
  log.info('Executing {cmd}'.format(**locals()))
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
  # alternately, if trapping is conditional:
  # if trap:
  #   stdout = stdout.decode('utf-8')
  #   stderr = stderr.decode('utf-8')
  rc = p.wait()
  log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

def extract(root, path):
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
    return extract(root, path)
  else:
    return root

parser = argparse.ArgumentParser(description='Discover AWS/GCP instances')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()
# log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

basename = os.path.basename(sys.argv[0])
if basename.endswith('.py'):
  basename = basename[:-3]
config_name = os.path.join(os.environ['HOME'], basename + '.json')
log.debug(f'config_name={config_name!r}')
if os.path.isfile(config_name):
  with open(config_name) as stream:
    try:
      config = json.load(stream)
    except Exception as e:
      parser.error(f'Could not parse {config_name!r}: "{e!s}"')
    log.debug(f'config: {config}')
else:
  log.warn('Could not find config {config_name!r}')
  config = {}

name_regexp = re.compile(config.get('regexp', '.'))
remove_regexp = bool(config.get('remove_regexp', 'false'))

if 'gcp_user' not in config:
  config['gcp_user'] = getpass.getuser()
  log.info('Assuming gcp_user={}'.format(config['gcp_user']))

instances = []

provider = 'aws'
(rc, stdout, stderr) = run('aws ec2 describe-instances')
if rc == 0 and stdout:
  raw = json.loads(stdout)
  for raw_reservation in raw.get('Reservations', []):
    for instance in raw_reservation.get('Instances', []):
      id = instance.get('InstanceId')

      name = None
      image_id = None
      image_name = None
      distro = None
      user = None
      ip = extract(instance, 'NetworkInterfaces/0/Association/PublicIp')
      active = extract(instance, 'State/Name') == 'running'

      if not id:
        parser.error(f'No instance ID in {instance}')
      log.info(f'aws instance id: {id}')
      name = None
      for tag in instance.get('Tags', []):
        log.debug(f'Examing tag {tag}')
        if tag.get('Key') == 'Name':
          name = tag.get('Value')
          break
      if name:
        log.info(f'instance name: {name}')
        match = name_regexp.search(name)
        if match:
          log.debug(f'instance {name} is desired')
          if remove_regexp:
            name = name[:match.start(0)] + name[match.end(0):]
            log.debug(f'after removing regular expression, instance name is {name}')

          image_id = instance.get('ImageId')
          log.debug(f'Instance {name} ({id}) uses image {image_id}')

          instances.append(Instance(provider, name, id, image_id, image_name, distro, user, ip, active))
      else:
        log.debug(f'No name for instance {id}')

backfill_aws_image_info(instances)

provider = 'gcp'
(rc, stdout, stderr) = run('gcloud --format json compute instances list')
if rc == 0 and stdout:
  raw = json.loads(stdout)
  for instance in raw:
    id = instance.get('id')

    image_id = None
    image_name = None
    distro = None
    user = None
    ip = extract(instance, 'networkInterfaces/0/accessConfigs/0/natIP')
    active = instance.get('status') == 'RUNNING'

    log.info(f'gcp instance id: {id}')
    name = instance.get('name', '')
    match = name_regexp.search(name)
    if match:
      log.debug(f'instance {name} is desired')
      if remove_regexp:
        name = name[:match.start(0)] + name[match.end(0):]
        log.debug(f'after removing regular expression, instance name is {name}')
        disks = instance.get('disks', [])
        if disks:
          instances.append(Instance(provider, name, id, disks[0].get('deviceName'), image_name, distro, user, ip, active))
        else:
          log.info(f'No device name for {id}/{name}')

backfill_gcp_image_info(instances)

log.debug('instances: {}'.format([instance.__dict__ for instance in instances]))
