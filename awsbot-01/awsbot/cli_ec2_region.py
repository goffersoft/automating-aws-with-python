#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Region CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_region import EC2RegionManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from ec2_region import EC2RegionManager
    from ec2_session import EC2SessionManager


def cli_ec2_region_init():
    """Initialize awsbot cli for ec2 regions."""
    pass


@click.group('region')
@cli_context
def cli_ec2_region(session=None):
    """- EC2 region CLI Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_region.command('list')
@click.option('--region-names', default=None,
              help='list of (comma separated) region names to list')
@cli_context
def list_regions(session, region_names):
    """List EC2 regions."""
    aok, err = EC2RegionManager(session.get_ec2_session()).\
        list_regions(region_names)

    if not aok:
        print(err)


if __name__ == '__main__':
    cli_ec2_region_init()
    cli_ec2_region()
