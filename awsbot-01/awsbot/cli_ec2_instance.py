#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Instance Related CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_instance import EC2InstanceManager
except ImportError:
    from cli_context import cli_context
    from ec2_instance import EC2InstanceManager


@click.group('instance')
@cli_context
def ec2_instance(session):
    """- AWS EC2 instances Automation Commands."""
    pass


@ec2_instance.command('list')
@click.option('--instances', default=None,
              help='list the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='list all instances for '
                   'project tag:Project:<name>')
@cli_context
def list_instances(session, instances, project_name):
    """List EC2 instances."""
    aok, err = EC2InstanceManager(session.get_ec2_session()).\
        list_instances(instances, project_name)

    if not aok:
        print(err)


@ec2_instance.command('start')
@click.option('--instances', default=None,
              help='start the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--force', is_flag=True,
              help='start all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='start all instances for project tag:Project:<name>')
@cli_context
def start_instances(session, instances, force, project_name):
    """Start EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    _, err = EC2InstanceManager(session.get_ec2_session()).\
        start_instances(instances, project_name)

    print()
    print(err)


@ec2_instance.command('stop')
@click.option('--instances', default=None,
              help='stop the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--force', is_flag=True,
              help='stop all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='stop all instances for project tag:Project:<name>')
@cli_context
def stop_instances(session, instances, force, project_name):
    """Stop EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    _, err = EC2InstanceManager(session.get_ec2_session()).\
        stop_instances(instances, project_name)

    print()
    print(err)


@ec2_instance.command('reboot')
@click.option('--instances', default=None,
              help='reboot the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--force', is_flag=True,
              help='reboot all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='reboot all instances for project tag:Project:<name>')
@cli_context
def reboot_instances(session, instances, force, project_name):
    """Reboot EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    _, err = EC2InstanceManager(session.get_ec2_session()).\
        reboot_instances(instances, project_name)

    print()
    print(err)


if __name__ == '__main__':
    pass
