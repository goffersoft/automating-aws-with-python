#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Security Group Automation CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.cli_ec2_security_group_rule import cli_ec2_security_group_rule
    from awsbot.cli_ec2_security_group_rule \
        import cli_ec2_security_group_rule_init
    from awsbot.ec2_security_group import EC2SecurityGroupManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from cli_ec2_security_group_rule import cli_ec2_security_group_rule
    from cli_ec2_security_group_rule import cli_ec2_security_group_rule_init
    from ec2_security_group import EC2SecurityGroupManager
    from ec2_session import EC2SessionManager


def cli_ec2_security_group_init():
    """Initialize awsbot cli for ec2 security groups."""
    cli_ec2_security_group_rule_init()
    cli_ec2_security_group.add_command(cli_ec2_security_group_rule)


@click.group('security-group')
@cli_context
def cli_ec2_security_group(session=None):
    """- AWS EC2 Security Group Automation Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_security_group.command('list')
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


@cli_ec2_security_group.command('create')
@click.argument('group-names')
@click.argument('vpc-ids')
@click.option('--descriptions', default=None,
              help='short description of the security group')
@cli_context
def create_security_groups(session, group_names, vpc_ids, descriptions):
    """Create Security groups."""
    _, status = EC2SecurityGroupManager(session.get_ec2_session()).\
        create_security_groups(group_names, vpc_ids, descriptions)

    print()
    print(status)


@cli_ec2_security_group.command('delete')
@click.argument('groups')
@cli_context
def delete_security_groups(session, groups):
    """Delete Security group.

    Delete security groups associated with (comma separated) groups.
    Can be group ids or group names of a mix of both'.
    """
    _, status = EC2SecurityGroupManager(session.get_ec2_session()).\
        delete_security_groups(groups)

    print()
    print(status)


if __name__ == '__main__':
    cli_ec2_security_group_init()
    cli_ec2_security_group()
