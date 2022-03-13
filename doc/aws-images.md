# `aws-images`

## Purpose
Search for Amazon EC2 AMIs.

## Syntax
```
Syntax: aws-images [--glob] [--region REGION ] 
        --owner OWNER_ID --name NAME_PATTERN
```

## Options and Arguments
| Option           | Description                                                                                                                                | Default                                                                                                                 |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `-g`, `--glob`   | Pattern is in the style of [filename expansion](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html) in a Linux shell | Pattern is in the style of a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) like used by `grep` |
| `-r`, `--region` | Override the AWS EC2 region                                                                                                                | The default region set in your AWS credentials is used.  I think a default region does not need to chosen in an AWS configuration but that I believe a default is very common and I know it's very useful.                                                                   
| `-v`             | Enable verbose debugging                                                                                                                   | Debugging is not enabled                                                                                                |


## Examples
I found the AWS owner by looking at the details of an Ubuntu AMI.  See the [`aws-image` example](aws-image.md)

### All images from the owner
You could use a simple name pattern that will match everything to show all images.
```
$ aws-images -o 099720109477 -n . | headtail
       1 Image name                                                                                              Image ID               Created
       2 ubuntu/images-testing/hvm-ssd/ubuntu-jammy-daily-amd64-server-20220313                                  ami-048161b37204478fd  2022-03-13T07:40:45.000Z
       3 ubuntu/images-testing/hvm-ssd/ubuntu-jammy-daily-arm64-server-20220313                                  ami-0ff349ebceeced8a1  2022-03-13T07:40:14.000Z
       4 ubuntu/images-testing/hvm-ssd/ubuntu-focal-daily-arm64-server-20220310                                  ami-051b53650d31ab7dc  2022-03-11T00:43:37.000Z
       5 ubuntu/images-testing/hvm-ssd/ubuntu-focal-daily-amd64-server-20220310                                  ami-02cba2b076a57c1ff  2022-03-11T00:43:12.000Z
         .
         .
         .
   14605 ubuntu-lucid-amd64-linux-image-2.6.32-301-ec2-v-2.6.32-301.4-ramdisk.20100108.smoser0.img               ari-64d73a0d           2010-01-08T08:28:04.000Z
   14606 ubuntu-lucid-i386-linux-image-2.6.32-301-ec2-v-2.6.32-301.4-ramdisk.20100108.smoser0.img                ari-86d439ef           2010-01-08T08:05:36.000Z
   14607 ubuntu-lucid-i386-linux-image-2.6.32-300-ec2-v-2.6.32-300.1-ramdisk.20100104.smoser0.img                ari-caf11ca3           2010-01-04T22:13:54.000Z
   14608 ubuntu-lucid-amd64-linux-image-2.6.32-300-ec2-v-2.6.32-300.1-ramdisk.20100104.smoser0.img               ari-14f11c7d           2010-01-04T21:55:21.000Z
   14609 
$ 
```

### Showing specific releases
You can specify more to the pattern to select only certain images.
```
$ aws-images -o 099720109477 -n 'ubuntu-.*-20.10-arm64' | headtail
       1 Image name                                                         Image ID               Created
       2 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210720    ami-0e7a5554e82452478  2021-07-21T13:02:53.000Z
       3 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210622    ami-0d57f0639aae57eb6  2021-06-22T20:12:19.000Z
       4 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210611    ami-09b84ecaca8c6d392  2021-06-11T14:16:27.000Z
       5 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210609    ami-0c6d6b37f76083978  2021-06-09T14:28:07.000Z
         .
         .
         .
      23 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201126    ami-01069be104eb25898  2020-11-27T17:48:38.000Z
      24 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201111    ami-01fd91c5afea9ccb1  2020-11-11T22:26:14.000Z
      25 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201030    ami-06284dd7c2ed5d8e7  2020-10-30T15:03:17.000Z
      26 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201022.1  ami-0ef42a98ef49bbb52  2020-10-22T18:04:02.000Z
      27 
$ 
```

### Using `--glob` pattern
A `glob` pattern works a little differently:
- The biggest difference is that a `glob` pattern is _anchored_ on both ends so you likely need wildcards at the start and finish.
- The `*` `glob` metacharacter does not apply to the previous regular expression so it's slightly easier to use.
```
$ aws-images -o 099720109477 -g -n '*ubuntu-*-20.10-arm64*' | headtail
       1 Image name                                                         Image ID               Created
       2 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210720    ami-0e7a5554e82452478  2021-07-21T13:02:53.000Z
       3 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210622    ami-0d57f0639aae57eb6  2021-06-22T20:12:19.000Z
       4 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210611    ami-09b84ecaca8c6d392  2021-06-11T14:16:27.000Z
       5 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20210609    ami-0c6d6b37f76083978  2021-06-09T14:28:07.000Z
         .
         .
         .
      23 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201126    ami-01069be104eb25898  2020-11-27T17:48:38.000Z
      24 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201111    ami-01fd91c5afea9ccb1  2020-11-11T22:26:14.000Z
      25 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201030    ami-06284dd7c2ed5d8e7  2020-10-30T15:03:17.000Z
      26 ubuntu/images/hvm-ssd/ubuntu-groovy-20.10-arm64-server-20201022.1  ami-0ef42a98ef49bbb52  2020-10-22T18:04:02.000Z
      27 
$ 
```

## Notes

- This script uses the [aws CLI](https://aws.amazon.com/cli/) and requires that you have installed it and set it up.
- The output is sorted by the the creation date of the image so the most recent is at the top.  I'm typically most interested in the latest image.