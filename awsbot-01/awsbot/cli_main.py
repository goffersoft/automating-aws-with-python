#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

import click

try:
    from awsbot.s3_region import S3RegionConfig
    from awsbot.cli_context import cli_context
except ImportError:
    from s3_region import S3RegionConfig
    from cli_context import cli_context


@click.group()
@click.option('--profile', default='python_automation',
              help='profile name to use while creating a boto3 session')
@click.option('--region', default=None,
              help='overide the region name in the aws profile')
@click.option('--s3-config', default='config/s3_region.csv',
              help='s3 region config csv file to use')
@cli_context
def cli(session, profile, region, s3_config):
    """Awsbot cli - AWS Automation Tool CLI."""
    region_config = None

    try:
        region_config = S3RegionConfig(s3_config)
    except FileNotFoundError as file_err:
        print('WARNING : Cannot load s3 endpoints' +
              f'from file {s3_config} : {str(file_err)}')

    session.init(profile, region, region_config)


if __name__ == '__main__':
    pass
