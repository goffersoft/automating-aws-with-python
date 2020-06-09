#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Security Group Automation CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_security_group import EC2SecurityGroupManager
except ImportError:
    from cli_context import cli_context
    from ec2_security_group import EC2SecurityGroupManager


@click.group('security-group')
@cli_context
def ec2_security_group(session):
    """- AWS EC2 Security Group Automation Commands."""
    pass


@ec2_security_group.command('list')
@cli_context
@click.option('--long', is_flag=True,
              help='print out rule info as well')
def list_security_groups(session, long):
    """List All Security groups."""
    ok, err = EC2SecurityGroupManager(session.get_ec2_session()).\
        list_security_groups(long)

    if not ok:
        print(err)


if __name__ == '__main__':
    pass
