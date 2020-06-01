# automating-aws-with-python

## awsbot-01

awsbot-01 is a script that will sync a local directory to a s3 bucket and optionally confiure route53 and cloudfront as well.

### Features
Awsbot has the following features 

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
