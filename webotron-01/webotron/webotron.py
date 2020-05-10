import click
from boto3_s3_helper import *


@click.group()
@click.option('--profile', default='python_automation',
              help='profile name to use while initializing the boto3 package')
@click.option('--region', default=None,
              help='overide the region name in the aws profile')
def cli(profile, region):
    """ Webotron - AWS Automation Tool """

    init(profile, region)


@cli.group()
def s3():
    """ - AWS S3 Automation Commands """

    pass


@s3.command('list-buckets')
def list_s3_buckets():
    """ List all S3 buckets """

    for bucket in get_s3_bucket_resources():
        print(bucket)


@s3.command('list-bucket-objects')
@click.argument('name', default=None)
def list_s3_bucket_objects(name):
    """ List all S3 bucket objects associated with bucker name """

    for obj in get_s3_bucket_resource(name).objects.all():
        print(obj)


@s3.command('setup-bucket')
@click.argument('name', default=None)
@click.option('--policy-file', default='templates/policy/allow_all.json',
              help='policy filename(contains a json document)\
                    or a json policy string')
@click.option('--index_file', default='templates/www/index.html',
              help='filename(contains a html document) or a html string')
@click.option('--index_name', default='index.html',
              help='name to use for the index s3 object')
@click.option('--error_file', default='templates/www/error.html',
              help='filename(contains a html document) or a html string')
@click.option('--error_name', default='error.html',
              help='name to use for the error s3 object')
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


@s3.command('sync-bucket')
@click.argument('path', default=None, type=click.Path(exists=True))
@click.argument('name', default=None)
@click.option('--validate', default=False, is_flag=True)
def s3_bucket_sync(path, name, validate):
    """ sync filesystem to s3 bucket

            sync files found in fs specified by 'fs_pathname' to bucket
            specified by 'bucket_name'.  optionally validate files (html only)
    """

    ok, err = sync_fs_to_s3_bucket(path, name, validate)

    if not ok:
        print(f'Cannot sync file system with bucket : {name} : {err}')
        return

    print(f'Bucket Sync Complete for s3 bucket : {name}')


if __name__ == '__main__':
    cli()
