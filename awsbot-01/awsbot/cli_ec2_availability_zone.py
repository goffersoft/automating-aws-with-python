#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Availability Zones CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_availability_zone import EC2AvailabilityZoneManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from ec2_availability_zone import EC2AvailabilityZoneManager
    from ec2_session import EC2SessionManager


def cli_ec2_availability_zone_init():
    """Initialize awsbot cli for ec2 availability zones."""
    pass


@click.group('availabilty-zone')
@cli_context
def cli_ec2_availability_zone(session=None):
    """- EC2 availability zone CLI Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_availability_zone.command('list')
@cli_context
def list_availability_zones(session):
    """List EC2 availability zones.

    List Availability Zones for the current region only.
    """
    aok, err = \
        EC2AvailabilityZoneManager(session.get_ec2_session()).\
        list_availability_zones()

    if not aok:
        print(err)


if __name__ == '__main__':
    cli_ec2_availability_zone_init()
    cli_ec2_availability_zone()
