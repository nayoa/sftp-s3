import os
import shutil
import pysftp
import boto3

def main():
    """
    Create directory using variable to temporarily store CSV reports

    Kick off script
    """

    directory = 'transfer'

    try:
        os.mkdir(directory)
        print(directory, "directory created")
    except FileExistsError:
        print(directory, "directory already exists")

    connect_to_sftp(directory)


def connect_to_sftp(directory):
    """
    Connects to sftp server using local environment variables
    """ 

    hostname = os.environ['HOST']
    username = os.environ['USER']
    password = os.environ['PASS']

    print('Connecting to Shipup SFTP server')
    sftp = pysftp.Connection(host=hostname, username=username, password=password)

    print('Established connection to SFTP server')

    get_csv_files(sftp, directory)

        
def get_csv_files(sftp, directory):
    """
    Copies the reports from the 'reports' directory on the SFTP server.

    The reports are copied to a local temp folder 'transfer'
    """

    print('Retrieving new csv reports')

    try:
        sftp.get_d('reports', 'transfer', preserve_mtime=True)
        print("CSV reports copied")
        upload_file_to_s3(directory)
    except ValueError as err:
        print("Nothing to copy")
        print(err.args)
        sftp.close()


def upload_file_to_s3(directory):
    """
    List the CSV reports in the temp directory

    Copy all reports to AWS S3
    """

    bucket = os.environ['BUCKET_NAME']
    s3_connect = boto3.client('s3')
    local_path = os.getcwd() # Get current working directory

    try:
        for filename in os.listdir(directory):
            file_key_name = filename
            local_name = local_path + '/' + directory + '/' + filename
            s3_connect.upload_file(local_name, bucket, file_key_name)
        print("Copied reports to S3 Succesfully")
        cleanup(directory)
    except ValueError as err:
        print("Unable to copy reports to S3")
        print(err.args)


def cleanup(directory):
    """
    Remove local directory with CSV reports
    """

    try: 
        shutil.rmtree(directory)
        print("Clean up complete")
    except ValueError as err:
        print("Nothing to clean up")
        print(err.args)


# def archive(sftp):]
        # """
        # Archive reports copied to S3 on SFTP server
        # """
#     for filename in sftp.listdir('reports'):
#         new_path = 'archive' + '/' + filename
#         sftp.rename(filename, new_path)
#         print("Move CSV files to Archive")
#         sftp.close()
#     else: 
#         print("Unable to archive")

# archive(sftp)
main()