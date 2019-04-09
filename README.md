# Shipup SFTP Transfer to S3

This repository contains a Python 3 script that connects to the shipup SFTP server and copies the latest CSV reports (France and UK) to an AWS S3 bucket. It grabs the latest CSV reports and archives the files on the SFTP server once the transfer to S3 is complete. It also cleans up the local CSV reports.

## Why

[shipup](https://www.shipup.co/) sends daily reports in CSV format to an SFTP server. We then want to analyse the reports in Big Query. In order to do this, the reports are sent to AWS S3 where a FiveTran Connection is set up to forward the data to Big Query. This repository automates the process of sending the reports to Amazon S3 and uses [gitlab-ci](.gitlab-ci.yml) to schedule the script to run at 2 am.

### Prerequisites

Install and export the below dependencies to run the script locally:

```shell
$ brew install python
$ brew install awscli
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo python3 get-pip.py
$ pip3 install -r requirements.txt
```

```shell
# Change the environment variables to match the SFTP server and AWS S3 bucket of choice.
$ export USER=<SFTP-USERNAME>
$ export PASS=<SFTP-PASSWORD>
$ export HOST=<SFTP-HOST>
$ export BUCKET_NAME=<SFTP-BUCKET-NAME>
```

**Note:** It is assumed that you are running MacOS and using [homebrew](https://brew.sh/) for installing packages.

Have programmatic access to Eve's AWS account (currently Production)

Export your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` of the AWS account you want to upload the CSV reports to.

**OR**

Ensure your credentials are in your `~/.aws/credentials` file.

If they're not, you can add them by doing:

```shell
$ aws configure
AWS Access Key ID []: <enter-aws-access-key>
AWS Secret Access Key []: <enter-aws-secret-key>
Default region name []: <enter-region-id> # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions
Default output format []: <leave-blank>
```

You can then check your CLI is using the correct credentials by doing:

```shell
$ aws sts get-caller-identity
```

## Run the script

```shell
$ python3 shipup-s3-transfer.py
```

### Potential Improvements

* Unit tests
* Improve the quality of Python code. e.g. Remove global variables, add classes and use different modules
* Change the script into an ansible playbook

### Built With

* [Python 3](https://www.python.org/download/releases/3.0/) - The programming language used
* [Pysftp](https://pysftp.readthedocs.io/en/release_0.2.9/) - Module/Library used to connect to SFTP and download reports
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Module/Library used to connect to AWS and upload reports to S3
