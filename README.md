# Shipup SFTP Transfer to S3

This repository contains a Python 3 script that connects to the shipup SFTP server and copies the latest CSV files to an AWS S3 bucket. It searches CSV files by date and archives the files on the SFTP server once the transfer to S3 is complete. It also cleans up the local CSV files.

## Why

[shipup](https://www.shipup.co/) sends daily reports in CSV format to an SFTP server. We then want to analyse the reports in Big Query. In order to do this, the reports are sent to AWS S3 where a FiveTran Connection is set up to forward the data to Big Query. This repository automates the process of sending the reports to Amazon S3 and uses a Jenkinsfile to schedule the script to run at 2 am.

### Prerequisites

Install and export the below dependencies to run the script locally:

```shell
$ brew install python
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo python3 get-pip.py
$ pip3 install -r requirements
```

```shell 
# Change the environment variables to match the SFTP server and AWS S3 bucket of choice.
$ export USER=<SFTP-USERNAME>
$ export PASS=<SFTP-PASSWORD>
$ export HOST=<SFTP-HOST>
$ export BUCKET_NAME=<SFTP-BUCKET-NAME>
```

**Note:** It is assumed that you are running MacOS and using [homebrew](https://brew.sh/) for installing packages.

### Execution

```shell
$ python3 shipup-s3-transfer.py
```

## Potential Improvements

* Change the script into an ansible playbook

## Built With

* [Python3](https://www.python.org/download/releases/3.0/) - The programming language used