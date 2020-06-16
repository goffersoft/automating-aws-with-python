#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_session import EC2SessionManager
    from awsbot.cli_ec2_instance import cli_ec2_instance
    from awsbot.cli_ec2_instance import cli_ec2_instance_init
    from awsbot.cli_ec2_volume import cli_ec2_volume
    from awsbot.cli_ec2_volume import cli_ec2_volume_init
    from awsbot.cli_ec2_keypair import cli_ec2_keypair
    from awsbot.cli_ec2_keypair import cli_ec2_keypair_init
    from awsbot.cli_ec2_security_group import cli_ec2_security_group
    from awsbot.cli_ec2_security_group import cli_ec2_security_group_init
    from awsbot.cli_ec2_region import cli_ec2_region
    from awsbot.cli_ec2_region import cli_ec2_region_init
    from awsbot.cli_ec2_availability_zone import cli_ec2_availability_zone
    from awsbot.cli_ec2_availability_zone import cli_ec2_availability_zone_init
except ImportError:
    from cli_context import cli_context
    from ec2_session import EC2SessionManager
    from cli_ec2_instance import cli_ec2_instance
    from cli_ec2_instance import cli_ec2_instance_init
    from cli_ec2_volume import cli_ec2_volume
    from cli_ec2_volume import cli_ec2_volume_init
    from cli_ec2_keypair import cli_ec2_keypair
    from cli_ec2_keypair import cli_ec2_keypair_init
    from cli_ec2_security_group import cli_ec2_security_group
    from cli_ec2_security_group import cli_ec2_security_group_init
    from cli_ec2_region import cli_ec2_region
    from cli_ec2_region import cli_ec2_region_init
    from cli_ec2_availability_zone import cli_ec2_availability_zone
    from cli_ec2_availability_zone import cli_ec2_availability_zone_init


def cli_ec2_init():
    """Initialize awsbot cli for ec2."""
    cli_ec2_region_init()
    cli_ec2.add_command(cli_ec2_region)

    cli_ec2_availability_zone_init()
    cli_ec2.add_command(cli_ec2_availability_zone)

    cli_ec2_security_group_init()
    cli_ec2.add_command(cli_ec2_security_group)

    cli_ec2_keypair_init()
    cli_ec2.add_command(cli_ec2_keypair)

    cli_ec2_volume_init()
    cli_ec2.add_command(cli_ec2_volume)

    cli_ec2_instance_init()
    cli_ec2.add_command(cli_ec2_instance)


@click.group('ec2')
@cli_context
def cli_ec2(session=None):
    """- AWS EC2 Automation Commands."""
    session.set_ec2_session(EC2SessionManager(session))


if __name__ == '__main__':
    cli_ec2_init()
    cli_ec2()
