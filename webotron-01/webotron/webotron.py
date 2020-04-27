import boto3
import sys
import click

g_session = boto3.Session(profile_name='python_automation')
g_ec2_resource = g_session.resource('ec2')
g_s3_resource = g_session.resource('s3')
#g_ec2_client = g_session.client('ec2')
#g_s3_client = g_session.client('s3')

@click.group()
def cli():
    pass

@cli.group()
def s3():
    pass

def get_s3_buckets():
   return g_s3_resource.buckets.all()

def get_s3_bucket(name):
   return g_s3_resource.Bucket(name)

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


