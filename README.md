# Shipup SFTP Transfer to S3

![coverage](https://gitlab.com/evesleep/shipup-sftp-s3/badges/master/pipeline.svg)

This repository contains a Python 3 script that connects to the shipup SFTP server and copies the latest CSV reports (France and UK) to an AWS S3 bucket. It grabs the latest CSV reports and archives the files on the SFTP server once the transfer to S3 is complete. It also cleans up the local CSV reports.

## Why

[shipup](https://www.shipup.co/) sends daily reports in CSV format to an SFTP server. We then want to analyse the reports in Big Query. In order to do this, the reports are sent to AWS S3 where a FiveTran Connection is set up to forward the data to Big Query. This repository automates the process of sending the reports to Amazon S3 and uses [gitlab-ci](.gitlab-ci.yml) to schedule the script to run at 2 am.

### Prerequisites

<details>
  <summary>
   What to install to use the module locally
  </summary>

**Note:**

* It is assumed that you are running MacOS and using [homebrew](https://brew.sh/) for installing packages.
* If you are using [zsh](https://ohmyz.sh/), echo the path and copy the virtualenv configuratrion into `~/.zshrc` instead of `~/.bashrc`.

Install brew dependencies:

* `$ brew list` shows what you already have installed.

```shell
$ brew update && brew upgrade
$ brew doctor
Your system is ready to brew.
$ brew install python
$ brew install awscli
```

Install the required pip packages:

```shell
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo python3 get-pip.py
```

Set Python3 as a default version of Python:

```shell
$ echo 'export PATH="/usr/local/opt/python/libexec/bin:/usr/local/sbin:$PATH"' >> ~/.bashrc
```

Install virtualenvwrapper:

```shell
$ pip install virtualenv
$ pip install virtualenvwrapper
```

Add virtualenvwrapper to shell startup file (~/.bashrc):

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Install pip requirements:

```shell
$ pip install -r requirements.txt
```

Export required environment variables:

```shell
# Change the environment variables to match the SFTP server and AWS S3 bucket of choice.
$ export USER=<SFTP-USERNAME>
$ export PASS=<SFTP-PASSWORD>
$ export HOST=<SFTP-HOST>
$ export BUCKET_NAME=<SFTP-BUCKET-NAME>
```

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
</details>

## Run the tests

```shell
$ pylint shipup_s3_transfer.py
```

## Run the script

```shell
$ python3 shipup_s3_transfer.py
```

### Potential Improvements

* Unit tests
* Improve the quality of Python code. e.g. Add classes and use different modules
* Change the script into an ansible playbook
* Create a custom docker base image with alpine packages and pip packages already installed

### Built With

* [Python 3](https://www.python.org/download/releases/3.0/) - The programming language used
* [Pysftp](https://pysftp.readthedocs.io/en/release_0.2.9/) - Module/Library used to connect to SFTP and download reports
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Module/Library used to connect to AWS and upload reports to S3
