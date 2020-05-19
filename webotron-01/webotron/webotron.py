#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various webotron commands."""

import click

try:
    from region_util import Region
    from boto3_session import Boto3SessionContext
    from boto3_s3_session import Boto3S3SessionContext
    from s3_bucket_manager import S3BucketManager
except ModuleNotFoundError:
    from .regionutil import Region
    from .boto3_session import Boto3SessionContext
    from .boto3_s3_session import Boto3S3SessionContext
    from .s3_bucket_manager import S3BucketManager


pass_context = click.make_pass_decorator(Boto3SessionContext,
                                         ensure=True)


@click.group()
@click.option('--profile', default='python_automation',
              help='profile name to use while initializing the boto3 package')
@click.option('--region', default=None,
              help='overide the region name in the aws profile')
@click.option('--config', default='config/region.csv',
              help='region config csv file to use')
@pass_context
def cli(session, profile, region, config):
    """Webotron - AWS Automation Tool."""
    region_config = None

    try:
        region_config = Region(config)
    except FileNotFoundError as file_err:
        print(f'WARNING : Cannot load s3 endpoints from \
              file {config} : {str(file_err)}')

    session.init(profile, region, region_config)


@cli.group()
@click.option('--chunk-size',
              default=8*1024*1024, type=click.INT,
              help='default s3 transfer chuck size')
@pass_context
def s3(session, chunk_size):
    """- AWS S3 Automation Commands."""
    session.set_s3_session_context(Boto3S3SessionContext(chunk_size))


@s3.command('list-buckets')
@pass_context
def list_s3_buckets(session):
    """List all S3 buckets."""
    S3BucketManager(session).list_buckets()


@s3.command('list-bucket-objects')
@click.argument('name', default=None)
@pass_context
def list_s3_bucket_objects(session, name):
    """List all S3 bucket objects associated with bucket name."""
    S3BucketManager(session).list_bucket_objects(name)


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
@pass_context
def s3_bucket_setup(session, name, policy_file, index_file,
                    index_name, error_file, error_name):
    """Set up a bucket for web hosting."""
    url, err = S3BucketManager(session).\
        setup_bucket(name, policy_file,
                     index_file, index_name,
                     error_file, error_name)

    if err is not None:
        print(f'Error Setting Up Bucket For Web Hosting : {name} : {err}')
    else:
        print(f'Bucket Setup Complete for s3 bucket : {name}')
        print(f'Bucket Website Url : {url}')


@s3.command('sync-bucket')
@click.argument('path', default=None, type=click.Path(exists=True))
@click.argument('name', default=None)
@click.option('--validate', default=False, is_flag=True)
@pass_context
def s3_bucket_sync(session, path, name, validate):
    """Sync filesystem to s3 bucket.

    sync files found in fs specified by 'fs_pathname' to bucket
    specified by 'bucket_name'.  optionally validate files (html only)
    """
    url, err = S3BucketManager(session).\
        sync_fs_to_bucket(path, name, validate)

    if err:
        print(f'Cannot sync file system with bucket : {name} : {err}')
    else:
        print(f'Bucket Sync Complete for s3 bucket : {name}')
        print(f'Bucket Website Url : {url}')


if __name__ == '__main__':
    cli()
