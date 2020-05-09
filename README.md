# automating-aws-with-python

## webotron-01

Webotron-01 is a script that will sync a local directory to a s3 bucket and optionally confiure route53 and cloudfront as well.

### Features
Webotron has the following features 

#### S3
    - list buckets
    - list bucket objects
    - setup bucket
        ```
        setup a bucket for web hosting
        1) create a bucket using the (required) bucket name
           and policy as a json string or file 
           default policy used if none provided
        2) add 2 html object to the bucket - index.html / error.html
           defaults used if none is provided
        3) enable web hosting on this bucket
        ```
        
