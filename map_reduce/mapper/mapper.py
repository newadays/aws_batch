#!/usr/bin/env python
import sys
import os
import uuid
import subprocess
import multiprocessing as mp
from multiprocessing import Pool,Process



sys.path.append('/lib')
# from lib.s3_utils import download_file, upload_file
# from lib.job_utils import generate_working_dir, delete_working_dir


# Get temp working dir
working_dir = os.getenv('working_dir', os.getcwd())
print('####################working_dir############################')
print(working_dir)

os.chdir(working_dir)

# creates subdirectory for the KDD data
data_dir = os.getcwd() + 'data'
print('####################data_dir############################')
print(data_dir)

try:
    os.makedirs(data_dir, mode=0o755)
except Exception as e:
    pass

# result = data_dir + '/' + 'result.txt'
# f = open(result, "w+")
# f.close()


def mapper(kdd_string):
    # http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names
    # Opens data directory and performs the mapper function
    result = []
    for line in kdd_string:
        '''
        removes unwanted characters then split using ','
        print(line.lower().strip('.\n').split(','))

        '''
        word = line.lower().strip('.\n').split(',')
        for letter in word:
            if letter == 'n':
                print('%s\t%s' % (letter, 1))
                print('WordCount\t1')
                result.append('{}   {}'.format(letter, 1))
    return result


def write_result(result_str):
    fd = open('/data/result.txt', "a")
    fd.write(result_str)
    fd.write('\n')
    fd.close()

# download the KDD data from s3 bucket into data dir
# local_data_path = download_folder('s3://profgbenga/data', data_dir)


if __name__ == "__main__":

    print('####################local_file_name############################')
    local_file_name = os.path.join(data_dir, 'kdd-200')
    print(local_file_name)

    # by default, parallelism expands s3 data to available cores exposed to the container
    # Read more about Python Parallelism here - https://docs.python.org/2/library/multiprocessing.html

    env_S3_SMILES = os.getenv('s3_kdd_data', 's3://profgbenga/data/kdd-200')
    s3_dn = subprocess.Popen("aws s3 cp {} {}".format(env_S3_SMILES, data_dir), shell=True)
    s3_dn.communicate()
    s3_file = env_S3_SMILES.split('/')[-1]
    infile = open(local_file_name, "r")
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    pool = mp.Pool()
    smiles_list = list(infile)
    # print(smiles_list)
    results = pool.map(mapper, smiles_list)
    print(len(results))
    pool.close()

    # Get the directory of the mapper results
    # result_file_path = mapper(local_data_path)

    # upload the intermediate result to
    # s3_file_path = 's3://profgbenga/result{}.txt'.format(str(uuid.uuid4()))
    # print(s3_file_path)
    # upload_file(s3_file_path, result_file_path)
    # print('Cleaning up working dir')
    # # delete the temp directory and all its local data
    # delete_working_dir(data_dir)
    print('Completed')