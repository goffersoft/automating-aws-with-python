### awsbot - aws cli commands

#### Introduction
```
Usage: awsbot [OPTIONS] COMMAND [ARGS]...

  Awsbot cli - AWS Automation Tool CLI.

Options:
  --profile TEXT    profile name to use while creating a boto3 session
  --region TEXT     overide the region name in the aws profile
  --s3-config TEXT  s3 region config csv file to use
  --help            Show this message and exit.

Commands:
  acm  - AWS ACM Automation Commands.
  cf   - AWS Cloud Front Automation Commands.
  cw   - AWS Cloudwatch Automation Commands.
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

#### Cloud Watch
```
Usage: awsbot.py cw [OPTIONS] COMMAND [ARGS]...

  - AWS Cloudwatch Automation Commands.

Options:
  --help  Show this message and exit.

Commands:
  alarm  - CloudWatch alarm cli commands.
```

##### Cloud Watch Alarms

    - list  List cloudwatch alarms.

#### EC2
```
Usage: awsbot ec2 [OPTIONS] COMMAND [ARGS]...

  - AWS EC2 Automation Commands.

Options:
  --help  Show this message and exit.

Commands:
  availabilty-zone  - EC2 availability zone CLI Commands.
  instance          - AWS EC2 instances Automation Commands.
  keypair           - AWS EC2 Key Pair Automation Commands.
  security-group    - AWS EC2 Security Group Automation Commands.
  region            - EC2 region CLI Commands.
  volume            - AWS EC2 instance volumes Automation Commands.
```

##### EC2 Availability Zone

    - list  List EC2 availability zones.

##### EC2 Instance 
    
    - create     Create one or more EC2 instances.
    - list       List EC2 instances.
    - modify     Modify EC2 instances.
    - reboot     Reboot EC2 instances.
    - start      Start EC2 instances.
    - stop       Stop EC2 instances.
    - terminate  Delete one or more or all EC2 instances.

##### EC2 KeyPair

    - create  Create KeyPair.
    - delete  Delete KeyPair.
    - import  Import KeyPair.
    - list    List All KeyPairs.

##### EC2 Security Group

    - create  Create Security group.
    - delete  Delete Security group. 
    - list    List All Security groups.
    - rule    - AWS EC2 Security Group Rules Automation Commands.

###### EC2 Security Group Rules

    - create  Create Security Group Rules.
    - delete  Delete Security Group Rules.

##### EC2 Region

    - list  List EC2 regions.

##### EC2 Volume

    - list  List volumes associated with all instances.
    - snapshot  - AWS EC2 volume snapshots Automation Commands.

###### EC2 Volume Snapshot

    - create  Create volume snapshots associated with selected instances.  
    - list    List snapshots associated with all volumes.
