#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Instance Related CLI commands."""

import click

try:
    from awsbot.cli_globals import pass_context
    from awsbot.ec2_instance import EC2InstanceManager
except ImportError:
    from cli_globals import pass_context
    from ec2_instance import EC2InstanceManager


@click.group('instance')
@pass_context
def ec2_instance(session):
    """- AWS EC2 instances Automation Commands."""
    pass


@ec2_instance.command('list')
@click.option('--instances', default=None,
              help='list the selected instances')
@click.option('--project-name', default=None,
              help='print all instances for '
                   'project tag:Project:<name>')
@pass_context
def list_instances(session, instances, project_name):
    """List EC2 instances."""
    ok, err = EC2InstanceManager(session.get_ec2_session()).\
        list_instances(instances, project_name)

    if not ok:
        print(err)


@ec2_instance.command('start')
@click.option('--instances', default=None,
              help='start the selected instances')
@click.option('--force', is_flag=True,
              help='start all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='start all instances for project tag:Project:<name>')
@pass_context
def start_instances(session, instances, force, project_name):
    """Start EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    ok, err = EC2InstanceManager(session.get_ec2_session()).\
        start_ec2_instances(instances, project_name)

    print()
    if ok and not err:
        print('Successfully Started All Instances')
    elif ok and err:
        print('Some Instances failed to start')
        print(err)
    else:
        print('Instances failed to start')
        print(err)


@ec2_instance.command('stop')
@click.option('--instances', default=None,
              help='stop the selected instances')
@click.option('--force', is_flag=True,
              help='stop all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='stop all instances for project tag:Project:<name>')
@pass_context
def stop_instances(session, instances, force, project_name):
    """Stop EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    ok, err = EC2InstanceManager(session.get_ec2_session()).\
        stop_ec2_instances(instances, project_name)

    print()
    if ok and not err:
        print('Successfully Stopped All Instances')
    elif ok and err:
        print('Some Instances failed to stop')
        print(err)
    else:
        print('Instances failed to stop')
        print(err)


if __name__ == '__main__':
    pass
