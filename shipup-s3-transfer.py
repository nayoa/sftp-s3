import os
import pysftp
import sys
import fnmatch
import datetime

def connect_to_sftp():

    hostname = os.environ['HOST']
    username = os.environ['USER']
    password = os.environ['PASS']

    today = datetime.date.today()

    file_pattern = f"*{today}*"

    print('Connecting to Shipup SFTP server')
    sftp = pysftp.Connection(host=hostname, username=username, password=password)

    print('Established connection to SFTP server')
        
def get_csv_files():

    print('Retrieving new csv files')
    with sftp.cd('reports'):

        for filenames in sftp.listdir():
            if fnmatch.fnmatch(filenames, file_pattern):
                print(filesnames)
        
        if sftp.exists(filenames) == True:
            sftp.get(filenames)
            print("csv files copied successfully")
        else:
            print("New csv files do not exist")


    sftp.close()

connect_to_sftp()
get_csv_files()


# def upload_file_to_s3():




# def archive():