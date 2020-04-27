import boto3
import sys
import click

g_boto3_session = None


def get_boto3_session():
    """ get boto3 session """
    return g_boto3_session


def get_resource(rname):
    """ get resource by input resource name """
    return get_boto3_session().resource(rname)


def get_client(cname):
    """ get client by input client name """
    return get_boto3_session().client(cname)


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


def init(pname='python_automation'):
    """ initialize webotron script """
    global g_boto3_session
    g_boto3_session = boto3.Session(profile_name=pname)


def get_s3_buckets():
    return get_s3_resource().buckets.all()


def get_s3_bucket(name):
    return get_s3_resource().Bucket(name)


@click.group()
def cli():
    init()


@cli.group()
def s3():
    pass


@s3.command('list-buckets')
def list_s3_buckets():
    """ List all S3 Buckets """
    for bucket in get_s3_buckets():
        print(bucket)


@s3.command('list-bucket-objects')
@click.argument('name')
def list_s3_bucket_objects(name):
    """ List all s3 bucket objects """
    for obj in get_s3_bucket(name).objects.all():
        print(obj)


if __name__ == '__main__':
    cli()
