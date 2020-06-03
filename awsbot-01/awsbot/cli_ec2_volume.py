#! /usr/bin/python
# -*- coding:utf-8 -*-


"""EC2 Instance volume Related CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_volume import EC2VolumeManager
except ImportError:
    from cli_context import cli_context
    from ec2_volume import EC2VolumeManager


@click.group('volume')
@cli_context
def ec2_volume(session):
    """- AWS EC2 instance volumes Automation Commands."""
    pass


@ec2_volume.command('list')
@click.option('--instances', default=None,
              help='reboot the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='reboot all instances for project tag:Project:<name>')
@cli_context
def list_volumes(session, instances, project_name):
    """List volumes associated with all instances."""
    ok, err = EC2VolumeManager(session.get_ec2_session()).\
        list_volumes(instances, project_name)

    if not ok:
        print(err)


if __name__ == '__main__':
    pass
