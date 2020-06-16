#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Availability Zones CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_availability_zone import EC2AvailabilityZoneManager
except ImportError:
    from cli_context import cli_context
    from ec2_availability_zone import EC2AvailabilityZoneManager


@click.group('availabilty-zone')
@cli_context
def ec2_availability_zone(session):
    """- EC2 availability zone CLI Commands."""
    pass


@ec2_availability_zone.command('list')
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
    pass
