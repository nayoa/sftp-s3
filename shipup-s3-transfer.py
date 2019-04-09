import os
import pysftp
import sys
import boto3
import fnmatch
import shutil

# Create directory to store CSV reports
directory = "transfer"

try:
    os.mkdir(directory)
    print(directory, "directory created")
except FileExistsError:
    print(directory, "directory already exists")

def connect_to_sftp():

    hostname = os.environ['HOST']
    username = os.environ['USER']
    password = os.environ['PASS']

    print('Connecting to Shipup SFTP server')
    global sftp
    sftp = pysftp.Connection(host=hostname, username=username, password=password)

    print('Established connection to SFTP server')
        
def get_csv_files(sftp):

    print('Retrieving new csv reports')

    try:
        sftp.get_d('reports', 'transfer', preserve_mtime=True)
        print("CSV reports copied")
        upload_file_to_s3()
    except ValueError as err:
        print("Nothing to copy")
        print(err.args)
        sftp.close()


def upload_file_to_s3():

# List of files in directory with CSV reports. 
# For Loop to upload files in directory and keep original naming convention

    bucket = os.environ['BUCKET_NAME']
    s3_connect = boto3.client('s3')

    local_path = os.getcwd() # Get current working directory

    try:
        for filename in os.listdir(directory):
            file_key_name = filename
            local_name = local_path + '/' + directory + '/' + filename
            s3_connect.upload_file(local_name, bucket, file_key_name)
        print("Copied reports to S3 Succesfully")
        print(file_key_name)
        cleanup()
    except ValueError as err:
        print("Unable to copy reports to S3")
        print(err.args)

def cleanup():

    try: 
        shutil.rmtree(directory)
        print("Clean up complete")
    except ValueError as err:
        print("Nothing to clean up")
        print(err.args)


# def archive(sftp):

#     for filename in sftp.listdir('reports'):
#         new_path = 'archive' + '/' + filename
#         sftp.rename(filename, new_path)
#         print("Move CSV files to Archive")
#         sftp.close()
#     else: 
#         print("Unable to archive")


connect_to_sftp()
get_csv_files(sftp)
# archive(sftp)
