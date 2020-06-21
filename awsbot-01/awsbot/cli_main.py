#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

import click

try:
    from awsbot.s3_region import S3RegionConfig
    from awsbot.cli_context import cli_context
    from awsbot.cli_s3 import cli_s3
    from awsbot.cli_s3 import cli_s3_init
    from awsbot.cli_r53 import cli_r53
    from awsbot.cli_r53 import cli_r53_init
    from awsbot.cli_acm import cli_acm
    from awsbot.cli_acm import cli_acm_init
    from awsbot.cli_cf import cli_cf
    from awsbot.cli_cf import cli_cf_init
    from awsbot.cli_ec2 import cli_ec2
    from awsbot.cli_ec2 import cli_ec2_init
    from awsbot.cli_cw import cli_cw
    from awsbot.cli_cw import cli_cw_init
except ImportError:
    from s3_region import S3RegionConfig
    from cli_context import cli_context
    from cli_s3 import cli_s3
    from cli_s3 import cli_s3_init
    from cli_r53 import cli_r53
    from cli_r53 import cli_r53_init
    from cli_acm import cli_acm
    from cli_acm import cli_acm_init
    from cli_cf import cli_cf
    from cli_cf import cli_cf_init
    from cli_ec2 import cli_ec2
    from cli_ec2 import cli_ec2_init
    from cli_cw import cli_cw
    from cli_cw import cli_cw_init


def cli_init():
    """Initialize cli.

    Configure click package
    """
    cli_acm_init()
    cli.add_command(cli_acm)

    cli_cf_init()
    cli.add_command(cli_cf)

    cli_ec2_init()
    cli.add_command(cli_ec2)

    cli_r53_init()
    cli.add_command(cli_r53)

    cli_s3_init()
    cli.add_command(cli_s3)

    cli_cw_init()
    cli.add_command(cli_cw)


@click.group()
@click.option('--profile', default='python_automation',
              help='profile name to use while creating a boto3 session')
@click.option('--region', default=None,
              help='overide the region name in the aws profile')
@click.option('--s3-config', default='config/s3_region.csv',
              help='s3 region config csv file to use')
@cli_context
def cli(session=None, profile=None, region=None, s3_config=None):
    """Awsbot cli - AWS Automation Tool CLI."""
    region_config = None

    try:
        region_config = S3RegionConfig(s3_config)
    except FileNotFoundError as file_err:
        print('WARNING : Cannot load s3 endpoints' +
              f'from file {s3_config} : {str(file_err)}')

    session.init(profile, region, region_config)


if __name__ == '__main__':
    cli_init()
    cli()
