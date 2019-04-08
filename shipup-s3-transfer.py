import os
import pysftp
import sys
import fnmatch
import datetime
import boto3

today = datetime.date.today()
file_pattern = f"*{today}*"

def connect_to_sftp():

    hostname = os.environ['HOST']
    username = os.environ['USER']
    password = os.environ['PASS']

    print('Connecting to Shipup SFTP server')
    global sftp
    sftp = pysftp.Connection(host=hostname, username=username, password=password)

    print('Established connection to SFTP server')
        
def get_csv_files(sftp):

    print('Retrieving new csv files')
    with sftp.cd('reports'):
        global filenames
        for filenames in sftp.listdir():
            if fnmatch.fnmatch(filenames, file_pattern):
                print(filenames)
        
        if sftp.exists(filenames) == True:
            sftp.get(filenames)
            print("CSV files copied")
            upload_file_to_s3(filenames)
        else:
            print("New CSV files do not exist")
            sftp.close()


def upload_file_to_s3(filenames):

    bucketName = os.environ['BUCKET_NAME']
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(filenames, bucketName, filenames)

    print("Copied to S3 Succesfully")
    return True


def archive(sftp, filenames):

    if upload_file_to_s3(filenames):
        sftp.rename(filenames, archive)
        print("Move CSV files to Archive")
        sftp.close()

def cleanup(filenames):

    if os.path.exists(filenames):
        os.remove(filenames)
        print("Clean up complete")
    else:
        print("Nothing to clean up")



connect_to_sftp()
get_csv_files(sftp)
# cleanup(filenames)
# archive(sftp, filenames)
