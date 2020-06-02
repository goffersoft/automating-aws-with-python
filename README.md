# automating-aws-with-python

#### Introduction
```
Usage: awsbot [OPTIONS] COMMAND [ARGS]...

  Awsbot cli - AWS Automation Tool CLI.

Options:
  --profile TEXT  profile name to use while creating a boto3 session
  --region TEXT   overide the region name in the aws profile
  --config TEXT   region config csv file to use
  --help          Show this message and exit.

Commands:
  acm  - AWS ACM Automation Commands.
  cf   - AWS Cloud Front Automation Commands.
  ec2  - AWS EC2 Automation Commands.
  r53  - AWS Route 53 Automation Commands.
  s3   - AWS S3 Automation Commands.
```
#### S3

    - list-bucket-objects  List S3 bucket objects
    - list-buckets         List all S3 buckets.
    - setup-bucket         Set up a bucket for web hosting.
        1) create a bucket using the (required) bucket name
           and policy as a json string or file 
           default policy used if none provided
        2) add 2 html object to the bucket - index.html / error.html
           defaults used if none is provided
        3) enable web hosting on this bucket
    - sync-bucket          Sync filesystem to s3 bucket.

#### Route 53

    - list-hosted-zones  List hosted zones.
    - list-record-sets   List Resource Record Sets.
    - setup-s3-domain    Create S3 domain.

#### ACM - Certificate Manager 

    - find-cert         Find cert that matches domain name.
    - get-cert-details  Get cert details.
    - list-cert-keys    Get cert keys.
    - list-certs        List certs.

#### Cloud Front

    - list-all-distributions  List all distributions.
    - list-distribution       List distribution matching domain name.
    - setup-s3-cdn            Create s3 cloud front distribution.

#### EC2
```
Usage: awsbot ec2 [OPTIONS] COMMAND [ARGS]...

  - AWS EC2 Automation Commands.

Options:
  --help  Show this message and exit.

Commands:
  instance  AWS EC2 instances Automation Commands.
```
##### EC2 Instance 

    - list   List EC2 instances.
    - start  Start EC2 instances.
    - stop   Stop EC2 instances.
