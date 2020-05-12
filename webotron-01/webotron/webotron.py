#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various webotron commands."""

import click

import boto3_s3_helper
import boto3_helper
import region_util


@click.group()
@click.option('--profile', default='python_automation',
              help='profile name to use while initializing the boto3 package')
@click.option('--region', default=None,
              help='overide the region name in the aws profile')
@click.option('--config', default='config/region.csv',
              help='region config csv file to use')
def cli(profile, region, config):
    """Webotron - AWS Automation Tool."""
    boto3_helper.init(profile, region)
    ok, err = region_util.init(config)

    if not ok:
        print(f'WARNING : Cannot load s3 endpoints from file {config} : {err}')


@cli.group()
def s3():
    """- AWS S3 Automation Commands."""
    pass


@s3.command('list-buckets')
def list_s3_buckets():
    """List all S3 buckets."""
    for bucket in boto3_s3_helper.get_s3_bucket_resources():
        print(bucket)


@s3.command('list-bucket-objects')
@click.argument('name', default=None)
def list_s3_bucket_objects(name):
    """List all S3 bucket objects associated with bucker name."""
    for obj in boto3_s3_helper.get_s3_bucket_resource(name).objects.all():
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
    """Set up a bucket for web hosting."""
    url, err = boto3_s3_helper.setup_s3_bucket(name, policy_file,
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
def s3_bucket_sync(path, name, validate):
    """Sync filesystem to s3 bucket.

    sync files found in fs specified by 'fs_pathname' to bucket
    specified by 'bucket_name'.  optionally validate files (html only)
    """
    url, err = boto3_s3_helper.sync_fs_to_s3_bucket(path, name, validate)

    if err:
        print(f'Cannot sync file system with bucket : {name} : {err}')
    else:
        print(f'Bucket Sync Complete for s3 bucket : {name}')
        print(f'Bucket Website Url : {url}')


if __name__ == '__main__':
    cli()
