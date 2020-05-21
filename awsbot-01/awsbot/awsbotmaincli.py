#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

import click

try:
    from awsbot.region_config import RegionConfig
    from awsbot.awsbotcliglobals import pass_context
except ImportError:
    from region_config import RegionConfig
    from awsbotcliglobals import pass_context


@click.group()
@click.option('--profile', default='python_automation',
              help='profile name to use while creatting a boto3 session')
@click.option('--region', default=None,
              help='overide the region name in the aws profile')
@click.option('--config', default='config/region.csv',
              help='region config csv file to use')
@pass_context
def cli(session, profile, region, config):
    """Webotron - AWS Automation Tool."""
    region_config = None

    try:
        region_config = RegionConfig(config)
    except FileNotFoundError as file_err:
        print(f'WARNING : Cannot load s3 endpoints from \
              file {config} : {str(file_err)}')

    session.init(profile, region, region_config)


if __name__ == '__main__':
    pass
