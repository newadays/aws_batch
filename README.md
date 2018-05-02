# aws_batch
Code Example of Running AWS Batch with Docker


* A word count example using map reduce on AWS Batch with docker to count words in large body of text e.g. mobydick, KDD dataset.
- You can learn more about cluster computing using AWS Batch using the link here -
https://aws.amazon.com/blogs/aws/aws-batch-run-batch-computing-jobs-on-aws/?nc1=b_rp
* The docker container can be setup using the commands in the commdands.txt file
- You can learn about using docker for python here - https://docs.docker.com/samples/library/python/#create-a-dockerfile-in-your-python-app-project
* The example leverage the multiprocessing in Python
- You can learn more about Multiprocessing in Python -  https://docs.python.org/2/library/multiprocessing.html

* By default, parallelism expands S3 data to available cores exposed to the container
* Batch computing will enable dynamically scale set of EC2 instances and run parallel jobs
* When setting up AWS Batch compute environment ensure to have minimum vcpus set to zero to prevent running on demand EC2 idle when there no jobs

### Quick Steps
1. Create a s3 bucket with folders for input and output data
2. Upload mobydick.txt (in the mapper folder) or KDD-dataset to the input folder of the s3 bucket
3. Note the s3 bucket url for input data and output folder e.g.  s3://mybucket/input/mobydick.txt & s3://mybucket/output
4. Setup your AWS Batch environment and ECS repository for Docker images - you can look into the commands.txt for AWS CLI commands
5. Specify the environment variables below and run the job 
* name: s3_input_dir, value: s3://mybucket/input/mobydick.txt
* name: s3_output_dir, value: s3://mybucket/output
* name: working_dir, value: /mapper


KDD-dataset - http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
