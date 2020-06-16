#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for s3 awsbot commands."""

import click

try:
    from awsbot.s3_session import S3SessionManager
    from awsbot.s3_bucket import S3BucketManager
    from awsbot.cli_context import cli_context
except ImportError:
    from s3_session import S3SessionManager
    from s3_bucket import S3BucketManager
    from cli_context import cli_context


@click.group()
@click.option('--chunk-size',
              default=8*1024*1024, type=click.INT,
              help='default s3 transfer chuck size')
@cli_context
def s3(session, chunk_size):
    """- AWS S3 Automation Commands."""
    session.set_s3_session(S3SessionManager(session, chunk_size))


@s3.command('list-buckets')
@cli_context
def list_s3_buckets(session):
    """List all S3 buckets."""
    aok, err = S3BucketManager(session.get_s3_session()).\
        list_buckets()

    if not aok:
        print(err)


@s3.command('list-bucket-objects')
@click.argument('name', default=None)
@cli_context
def list_s3_bucket_objects(session, name):
    """List all S3 bucket objects associated with bucket name."""
    aok, err = S3BucketManager(session.get_s3_session()).\
        list_bucket_objects(name)

    if not aok:
        print(err)


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
@cli_context
def s3_bucket_setup(session, name, policy_file, index_file,
                    index_name, error_file, error_name):
    """Set up a bucket for web hosting."""
    url, err = S3BucketManager(session.get_s3_session()).\
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
@click.option('--validate', default=False, is_flag=True,
              help='validates html file syntax before syncing with s3 bucket')
@cli_context
def s3_bucket_sync(session, path, name, validate):
    """Sync filesystem to s3 bucket.

    sync files found in fs specified by 'fs_pathname' to bucket
    specified by 'bucket_name'.  optionally validate files (html only)
    """
    url, err = S3BucketManager(session.get_s3_session()).\
        sync_fs_to_bucket(path, name, validate)

    if err:
        print(f'Cannot sync file system with bucket : {name} : {err}')
    else:
        print(f'Bucket Sync Complete for s3 bucket : {name}')
        print(f'Bucket Website Url : {url}')


if __name__ == '__main__':
    pass
