import click
from boto3_s3_helper import *


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
    """ setup a bucket for web hosting
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
