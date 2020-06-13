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
@click.option('--groups', default=None,
              help='filter by (comma separated) groups. ' +
              'can be group ids or group names of a mix of both')
@click.option('--long', is_flag=True,
              help='print out rule info as well')
@cli_context
def list_security_groups(session, groups, long):
    """List All Security groups."""
    aok, err = EC2SecurityGroupManager(session.get_ec2_session()).\
        list_security_groups(groups, long)

    if not aok:
        print(err)


@ec2_security_group.command('create')
@click.argument('group-name')
@click.argument('vpc-id')
@click.option('--description', default=None,
              help='short description of the security group')
@cli_context
def create_security_groups(session, group_name, vpc_id, description):
    """Create Security group."""
    _, status = EC2SecurityGroupManager(session.get_ec2_session()).\
        create_security_group(group_name, vpc_id, description)

    print(status)


@ec2_security_group.command('delete')
@click.argument('groups')
@cli_context
def delete_security_groups(session, groups):
    """Delete Security group.

    Delete security groups associated with (comma separated) groups.
    Can be group ids or group names of a mix of both'.
    """
    _, status = EC2SecurityGroupManager(session.get_ec2_session()).\
        delete_security_groups(groups)

    print(status)


if __name__ == '__main__':
    pass
