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
@click.option('--group-ids', default=None,
              help='filter by (comma separated) group-ids')
@click.option('--group-names', default=None,
              help='filter by (comma separated) group-names')
@click.option('--long', is_flag=True,
              help='print out rule info as well')
@cli_context
def list_security_groups(session, long, group_ids, group_names):
    """List All Security groups."""
    ok, err = EC2SecurityGroupManager(session.get_ec2_session()).\
        list_security_groups(group_ids, group_names, long)

    if not ok:
        print(err)


@ec2_security_group.command('create')
@click.argument('group-name')
@click.argument('vpc-id')
@click.option('--description', default=None,
              help='short description of the security group')
@cli_context
def create_security_groups(session, group_name, vpc_id, description):
    """Create Security group."""
    ok, err = EC2SecurityGroupManager(session.get_ec2_session()).\
        create_security_group(group_name, vpc_id, description)

    if not ok:
        print(err)


@ec2_security_group.command('delete')
@click.argument('group-id-or-name')
@click.option('--group-name-type', is_flag=True,
              help='indicates that (comma separated) arguments ' +
              'passed in are group names')
@cli_context
def delete_security_groups(session, group_id_or_name, group_name_type):
    """Delete Security group."""
    group_names = group_id_or_name if group_name_type else None
    group_ids = group_id_or_name if not group_name_type else None

    ok, status = EC2SecurityGroupManager(session.get_ec2_session()).\
        delete_security_groups(group_ids, group_names)

    print(status)


if __name__ == '__main__':
    pass
