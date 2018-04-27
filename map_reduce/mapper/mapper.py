#!/usr/bin/env python
'''
An code example of AWS Batch with docker to count words in large body of text e.g. mobydick, KDD dataset.
You can learn more about cluster computing using AWS Batch using the link here -
https://aws.amazon.com/blogs/aws/aws-batch-run-batch-computing-jobs-on-aws/?nc1=b_rp
The docker container can be setup using the commands in the commdands.txt file
You can learn about using docker for python here - https://docs.docker.com/samples/library/python/#create-a-dockerfile-in-your-python-app-project
The example leverage the multiprocessing in Python
You can learn more about Multiprocessing in Python -  https://docs.python.org/2/library/multiprocessing.html
'''

import sys
import os
import uuid
import subprocess
import multiprocessing as mp
from multiprocessing import Pool,Process

sys.path.append('/lib')
from lib.s3_utils import download_file, upload_file
from lib.job_utils import generate_working_dir, delete_working_dir


# Get temp working dir
working_dir = os.getenv('  ', os.getcwd())
print('####################working_dir############################')
print(working_dir)

os.chdir(working_dir)

# creates subdirectory for the KDD data
data_dir = working_dir + '/data'
print('####################data_dir############################')
print(data_dir)

try:
    os.makedirs(data_dir, mode=0o755)
except Exception as e:
    pass

# result = data_dir + '/' + 'result.txt'
# f = open(result, "w+")
# f.close()


def mapper(words):
    # http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names
    # Opens data directory and performs the mapper function
    result = []
    for line in words:
        '''
        removes unwanted characters then split using ','
        print(line.lower().strip('.\n').split(','))
        '''
        line = line.lower().strip('.\n').split(',')
        for word in line:
            result.append('{}, {}'.format(word, 1))

    return result


def write_result(result_str, dir):
    '''
    :param result_str: results to be written
    :param data_dir: local folder to write results
    :return path to the local result file
    '''
    results_path = os.path.join(dir, 'result-{}.txt'.format(str(uuid.uuid4())))
    fd = open(results_path, "w")
    for item in result_str:
        fd.write("%s\n" % item)
    fd.close()
    return results_path

# download the KDD data from s3 bucket into data dir
# local_data_path = download_folder('s3://profgbenga/data', data_dir)


if __name__ == "__main__":
    # s3 bucket & folder e.g. s3://mybucket/data
    s3_input_dir = ''
    s3_output_dir = ''
    try:
        s3_input_dir = os.getenv('s3_input_dir')
        s3_output_dir = os.getenv('s3_output_dir')
        input_file = os.getenv('input_file')
    except EnvironmentError:
        print("No s3 bucket information provided")

    print('####################local_file_name############################')
    local_file_name = os.path.join(data_dir, input_file)
    print(local_file_name)

    if s3_input_dir:

        # by default, parallelism expands s3 data to available cores exposed to the container
        # Read more about Python Parallelism here - https://docs.python.org/2/library/multiprocessing.html
        s3_proc = subprocess.Popen("aws s3 cp {} {}".format(s3_input_dir + '{}'.format(input_file),  local_file_name), shell=True)
        s3_proc.communicate()
        pool = mp.Pool()
        # s3_file = s3_input_dir.split('/')[-1]

        # Read downloaded file
        file = open(local_file_name, 'r')
        data = list(file)
        file.close()

        # The data source can be any dictionary-like object and convert list to be distributed
        datasource = dict(enumerate(data))
        input_data = [list(datasource.values())]
        results = pool.map(mapper, input_data)
        print(results)
        pool.close()

        # Get the directory of the mapper results

        # upload the intermediate result to s3 bucket
        result_file_path = write_result(results, data_dir)
        filename = result_file_path.split('/')[-1]
        print(filename)
        s3_output_file = s3_output_dir + filename
        print(s3_output_file)

        result_file_path = upload_file(s3_output_file, result_file_path)
        print('Cleaning up working dir')
        # delete the temp directory and all its local data
        delete_working_dir(data_dir)
        print('Completed')
    else:
        print("No s3 bucket information provided")
        sys.exit(0)
