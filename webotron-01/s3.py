# coding: utf-8
import boto3
session = boto3.Session(profile_name='python_automation')
s3 = session.resource('s3')
s3.Bucket('peasbucketwebsite')
session.region_name
bucket = s3.create_bucket(Bucket='peastestbucket', 
                         CreateBucketConfiguration={'LocationConstraint' : session.region_name})
bucket = s3.create_bucket(Bucket='peastestbucket')
bucket.upload_file('index.html', 'index.html', ExtraArgs={'ContentType' : 'text/html'})
def print_buckets():
    for i in s3.buckets.all():
        print(i)
        
print_buckets()
policy='''{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"PublicRead",
      "Effect":"Allow",
      "Principal": "*",
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::%s/*"]
    }
  ]
}''' % bucket.name
pol = bucket.Policy()
web = bucket.WebSite()
pol.put(Policy=policy)
web.put(WebsiteConfiguration={'IndexDocument': {
            'Suffix': 'index.html'
        },
        'ErrorDocument': {
            'Key': 'error.html'
        },
        }
        )
bucket_url =  'http://%s.s3-website-%s.amazonaws.com' % (bucket.name, session.region_name)

#pipenv install html5lib
import html5lib
parser = html5lib.Html5PArser(strict=True)
html5lib.parse('''<!doctype html>
    <html>
    <head>
    <title>This is the title of the webpage!</title>
    </head>
    <body>
    <p>This is an example paragraph. Anything in the <strong>body</strong> tag will appear on the page, just like this <strong>p</strong> tag and its contents.</p>
    </body>
    </html>''')
html5lib.parse('<html></html>')
#ParseError: Unexpected start tag (html). Expected DOCTYPE.

import json
j = """{
     "Version": "2012-10-17",
     "Statement": [
     {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::peastestbucket/*"
      }
    ]}"""
json.loads(j)
#JSONDecodeError: Expecting ',' delimiter: line 11 column 6 (char 263)
