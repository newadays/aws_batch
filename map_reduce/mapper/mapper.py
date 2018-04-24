#!/usr/bin/env python
import sys
import os
import uuid
import subprocess
import shlex

sys.path.append('/lib')
from lib.s3_utils import download_file, upload_file
from lib.job_utils import generate_working_dir, delete_working_dir


# http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names
labels = ['back', 'buffer_overflow', 'ftp_write', 'guess_passwd', 'imap', 'ipsweep', 'land', 'loadmodule',
              'multihop', 'neptune', 'nmap', 'normal', 'perl', 'phf', 'pod', 'portsweep', 'rootkit', 'satan', 'smurf',
              'spy', 'teardrop', 'warezclient', 'warezmaster']


# Get temp working dir
working_dir = os.getenv('working_dir', '/')
print('####################working_dir############################')
print(working_dir)

os.chdir(working_dir)


def mapper(local_path):
    # Opens data directory and performs the mapper function
    with open(local_path) as file:
        result_path = data_dir + '/' + 'result.txt'
        result = open(result_path, 'w+')
        for line in file:
            '''
            removes unwanted characters then split using ','
            print(line.lower().strip('.\n').split(','))

            '''
            words = line.lower().strip('.\n').split(',')
            for word in words:
                if word in labels:
                    print('%s\t%s' % (word, 1))
                    # print('WordCount\t1')
                    result.write('%s\t%s\r\n' % (word, 1))

        result.close()
    return result_path

# download the KDD data from s3 bucket into data dir
# local_data_path = download_folder('s3://profgbenga/data', data_dir)


if __name__ == "__main__":

    # creates subdirectory for the KDD data
    data_dir = os.getenv('data_dir', os.getcwd() + 'data')
    print('####################data_dir############################')
    if os.path.isdir(data_dir):
        pass
    else:
        try:
            os.makedirs(data_dir, mode=0o755)
        except Exception as e:
            pass

    print(data_dir)
    cmd = 'aws s3 cp --recursive %s %s' % ('s3://profgbenga/data', data_dir)

    local_data_path = subprocess.check_call(shlex.split(cmd), shell=True)

    print(local_data_path)

    # Get the directory of the mapper results
    result_file_path = mapper(local_data_path)

    # upload the intermediate result to
    s3_file_path = 's3://profgbenga/result{}.txt'.format(str(uuid.uuid4()))
    print(s3_file_path)
    upload_file(s3_file_path, result_file_path)
    print('Cleaning up working dir')
    # delete the temp directory and all its local data
    delete_working_dir(data_dir)
    print('Completed')