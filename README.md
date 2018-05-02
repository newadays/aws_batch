
# aws_batch
Code Example of Running Map Reduce Jobs on AWS Batch with Docker

![Alt map_reduce_word_count](https://github.com/newadays/aws_batch/blob/master/aws_batch_map_reduce.png)


* A map reduce example using map reduce on AWS Batch to count words in a large body of text e.g. [moby dick](https://en.wikipedia.org/wiki/Moby-Dick), [KDD-dataset](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
- You can learn more about cluster computing using AWS Batch using the link [here](https://aws.amazon.com/blogs/aws/aws-batch-run-batch-computing-jobs-on-aws/?nc1=b_rp)
* The docker container can be set up using the commands in the file [here](https://github.com/newadays/aws_batch/blob/master/map_reduce/commands.txt)

- You can learn about using Docker for python [here](https://docs.docker.com/samples/library/python/#create-a-dockerfile-in-your-python-app-project)
* The example leverage the multiprocessing in Python
- You can learn more about Multiprocessing in Python [here](https://docs.python.org/2/library/multiprocessing.html)

* By default, parallelism expands S3 data to available cores exposed to the container
* Batch computing will enable dynamically scale set of EC2 instances and run parallel jobs. When setting up AWS Batch compute environment ensure to have minimum VCPUs set to zero to prevent running on-demand EC2 idle when there no jobs

### Quick Steps
1. Create an S3 bucket with folders for input and output data
2. Upload mobydick.txt or KDD-dataset to the input folder of the s3 bucket
3. Note the S3 bucket URL for input data and output folder e.g.  s3://mybucket/data/mobydick.txt & s3://mybucket/result
4. Setup your AWS Batch environment and ECS repository for Docker images - look [here](https://github.com/newadays/aws_batch/blob/master/map_reduce/commands.txt) for AWS CLI commands
5. Specify the environment variables below and run the job 
* name: s3_input_dir, value: s3://mybucket/input/mobydick.txt
* name: s3_output_dir, value: s3://mybucket/output
* name: working_dir, value: /mapper


[moby dick](https://en.wikipedia.org/wiki/Moby-Dick)
[KDD-dataset](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
[AWS Batch](https://aws.amazon.com/batch/)
[AWS S3](https://aws.amazon.com/s3/)
[AWS ECR](https://aws.amazon.com/ecr/)
