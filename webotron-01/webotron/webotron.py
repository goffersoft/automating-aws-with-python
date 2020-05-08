import boto3
from botocore.exceptions import ClientError
import sys
import click
import json 
from json.decoder import JSONDecodeError
import html5lib
from html5lib.html5parser import ParseError

g_boto3_session = None
g_s3_bucket_url = 'http://%s.s3-website-%s.amazonaws.com'


def get_session():
    """ get boto3 session """

    return g_boto3_session


def get_resource(rname):
    """ get resource by input resource name """

    return get_session().resource(rname)


def get_client(cname):
    """ get client by input client name """

    return get_session().client(cname)


def get_ec2_resource():
    """ get ec2 resource """

    return get_resource('ec2')


def get_ec2_client():
    """ get ec2 client """

    return get_client('ec2')


def get_s3_resource():
    """ get s3 resource """

    return get_resource('s3')


def get_s3_client():
    """ get s3 client """

    return get_client('s3')


def get_s3_bucket_resources():
    """ get all s3 bucket resources as iterable """

    return get_s3_resource().buckets.all()


def get_s3_bucket_resource(name):
    """ get s3 bucket resource associated with name """

    return get_s3_resource().Bucket(name)


def get_s3_bucket_website_resource(bucket_resource):
    """ get s3 website resource associated with this bucket resource """

    return bucket_resource.Website()


def get_s3_bucket_policy_resource(bucket_resource):
    """ get s3 policy resource associated with this bucket resource """

    return bucket_resource.Policy()


def default_region():
    """ check to see if region associated with session is us-east-1(default)"""

    return get_session().region_name == 'us-east-1'


def getClientErrorCode(e):
    """ get client error code from the response """

    return e.response['Error']['Code']


def is_valid_s3_bucket_policy(policy):
    """ validdate the policy file or the policy string passed in """

    return is_valid_json(policy)


def is_valid_s3_bucket_object_html(html):
    """ validdate the bucket object as a valid html file or a string """

    return is_valid_html(html)


def s3_bucket_enable_webhosting(bucket_res, index_name, error_name):
    """ enbale web hosting on this bucket """

    try:
        web = get_s3_bucket_website_resource(bucket_res)

        web.put(WebsiteConfiguration=\
                 {'IndexDocument': { 'Suffix': index_name },\
                  'ErrorDocument': { 'Key': error_name }, })

        return True, None
    except ClientError as e: 
        return False, str(e)


def s3_bucket_cleanup(bucket_res):
    pass


def create_s3_bucket_policy(bucket_res, policy, validate=True):
    """ create/associate a policy with this 33 bucket """
     
    if validate:
        policy, err = validate_and_get_s3_bucket_policy_as_string(bucket_res.name, policy)
        
        if err is not None:
            return False, err

    try:
        get_s3_bucket_policy_resource(bucket_res).put(Policy=policy)
        return True, None;
    except ClientError as e:
        return False, str(e)

def validate_and_get_s3_bucket_policy_as_string(bucket_name, bucket_policy):
    """ validates the s3 bucket policy (file or a string)
        and return the s3 bucket policy as string
    """

    ok, type, err = is_valid_s3_bucket_policy(bucket_policy)

    if not ok:
        return None, err

    if type == 'file':
        bucket_policy, err = get_file_as_string(bucket_policy)
        if err is not None:
            return None, err

    return bucket_policy % bucket_name, None


def get_s3_bucket_url(bucket_name):
    return g_s3_bucket_url %(bucket_name, get_session().region_name)


def create_s3_bucket(name, policy):
    """ create a s3 bucket """

    bucket = None

    try:
        policy, err = \
               validate_and_get_s3_bucket_policy_as_string(name, policy)

        if err is not None:
            return None, err

        if default_region():
            bucket = get_s3_resource().create_bucket(Bucket=name)
        else:
            bucket = get_s3_resource().\
                      create_bucket(Bucket=name,
                           CreateBucketConfiguration=\
                    {'LocationConstraint' : get_session().region_name})

        ok, err = create_s3_bucket_policy(bucket, policy, False)

        if not ok:
            return None, f'Fatal : Cannot Create Bucket Policy : {err}'
            
    except ClientError as e:
        if getClientErrorCode(e) == 'BucketAlreadyOwnedByYou':
            bucket = get_s3_bucket_resource(name)
        else:
            return None, str(e) 

    return bucket, None


def create_s3_bucket_object_html(bucket_res, html, filename):
    """ create a s3 bucket (html) object """

    ok, type, err = is_valid_html(html)

    if not ok:
        return False, err

    try:
        if type == 'str':
            get_s3_resource().Object(bucket_res.name, filename).\
                                 put(Body=bytes(html),
                                     ContentType='text/html')
        else:
            bucket_res.upload_file(html, filename,
                              ExtraArgs={'ContentType' : 'text/html'})
    except ClientError as e:
        return False, str(e)

    return True, None


def get_file_as_string(filename):
    """  get the contents of a file as a string.
         raises the FileNotFoundException 
    """

    try:
        with open(filename) as file:
            return file.read(), None
    except FileNotFoundError as e:
        return None, str(e) 


def is_valid_html_file(html_file):
    """  validates the contents of the file as html 
         raises the FileNotFoundException 
    """
    with open(html_file) as file:
        try:
            parser = html5lib.HTMLParser(strict=True)
            parser.parse(file)

            return True, None
        except ParseError as e:
            return False, str(e)


def is_valid_html_string(html_string):
    """ validates the string passed in as html """

    try:
        parser = html5lib.HTMLParser(strict=True)
        parser.parse(html_string)

        return True, None
    except ParseError as e:
        return False, str(e)


def is_valid_json_file(json_file):
    """  validates the contents of the file as json
         raises the FileNotFoundException 
    """

    with open(json_file) as file:
        try:
            json.load(file)
            return True, None
        except JSONDecodeError as e:
            return False, str(e)


def is_valid_json_string(json_str):
    """ validates the string passed in as json """

    try:
        json.loads(json_str)
        return True, None
    except JSONDecodeError as e:
        return False, str(e)


def is_valid_html(html, type=None, estr=None):
    """ validates the filename or a string passed in as html """

    try:
        if (type == None or type == 'file'):
            ok, err = is_valid_html_file(html)
        else:
            ok, err = is_valid_html_string(html)

        if ok:
            return True, 'file' if type is None else 'str', None

        if (estr == None):
            return False, None, f'Invalid Json String: {err}'
        else:
            return False, None,\
                    f'Invalid file name or html string: str([{estr}, {err}])'
    except FileNotFoundError as e:
        return is_valid_html(html, 'str', str(e))


def is_valid_json(json, type=None, estr=None):
    """ validates the filename or a string passed in as json """

    try:
        if (type == None or type == 'file'):
            ok, err = is_valid_json_file(json)
        else:
            ok, err = is_valid_json_string(json)
        
        if ok: 
            return True, 'file' if type is None else 'str', None

        if (estr == None):
            return False, None, 'Invalid Json String:' + err
        else:
            return False, None,\
                    f'Invalid file name or json string: str([{estr}, {err}])'
    except FileNotFoundError as e:
        return is_valid_json(json, 'str', str(e))


def init(pname='python_automation', rname=None):
    """ initialize webotron script """

    global g_boto3_session

    if rname is None:
        g_boto3_session = boto3.Session(profile_name=pname)
    else:
        g_boto3_session = boto3.Session(profile_name=pname, region_name=rname)


@click.group()
def cli():
    """ cli (base) group -- entry point """

    init()


@cli.group()
def s3():
    """ s3 group -- cli-->s3 """

    pass


@s3.command('list-buckets')
def list_s3_buckets():
    """ List all S3 Buckets """

    for bucket in get_s3_bucket_resources():
        print(bucket)


@s3.command('list-bucket-objects')
@click.argument('name')
def list_s3_bucket_objects(name):
    """ List all s3 bucket objects """

    for obj in get_s3_bucket_resource(name).objects.all():
        print(obj)


@s3.command('setup-bucket')
@click.argument('name')
@click.argument('policy_file', default='templates/policy/allow_all.json')
@click.argument('index_file', default='templates/www/index.html')
@click.argument('index_name', default='index.html')
@click.argument('error_file', default='templates/www/error.html')
@click.argument('error_name', default='error.html')
def s3_bucket_setup(name, policy_file, index_file,
                    index_name, error_file, error_name):
    """ setup a buket for web hosting
        1) create a bucket using the (required) bucket name
           and policy as a json string or file 
           default policy used if none provided
        2) add 2 html object to the bucket - index.html / error.html
           defaults used if none is provided
        3) enable web hosting on this bucket
    """

    bucket_res, err = create_s3_bucket(name, policy_file)
    if err is not None:
        print(f'Cannot create bucket {name}: {err}')
        s3_bucket_cleanup(bucket_res)
        return
    
    ok, err = create_s3_bucket_object_html(bucket_res, index_file, index_name)
    if not ok:
        print(f'Cannot create bucket object {index} : {err}')
        s3_bucket_cleanup(bucket_res)
        return

    ok, err = create_s3_bucket_object_html(bucket_res, error_file, error_name) 
    if not ok:
        print(f'Cannot create bucket {error} : {err}')
        s3_bucket_cleanup(bucket_res)
        return
     
    ok, err = s3_bucket_enable_webhosting(bucket_res, index_name, error_name)
    if not ok:
        print(f'Cannot enable web hosting on bucket : {name} : {err}')
        s3_bucket_cleanup(bucket_res)
        return

    print(f'Bucket Setup Complete for s3 bucket : {name}')
    print(f'Bucket Website Url : {get_s3_bucket_url(name)}')


if __name__ == '__main__':
    cli()
