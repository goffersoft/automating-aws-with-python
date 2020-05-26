# automating-aws-with-python

## awsbot-01

awsbot-01 is a script that will sync a local directory to a s3 bucket and optionally confiure route53 and cloudfront as well.

### Features
Awsbot has the following features 

#### S3
    - list buckets
    - list bucket objects
    - setup bucket
        setup a bucket for web hosting
        1) create a bucket using the (required) bucket name
           and policy as a json string or file 
           default policy used if none provided
        2) add 2 html object to the bucket - index.html / error.html
           defaults used if none is provided
        3) enable web hosting on this bucket
    - sync web directory from filesystem with a s3 bucket 
#### R53
    - list-hosted-zones
    - list-record-sets
    - setup-s3-domain
