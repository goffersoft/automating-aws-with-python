#! /usr/bin/python
# -*- coding:utf-8 -*-


"""EC2 Instance volume Related CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.cli_ec2_volume_snapshot import cli_ec2_volume_snapshot_init
    from awsbot.cli_ec2_volume_snapshot import cli_ec2_volume_snapshot
    from awsbot.ec2_volume import EC2VolumeManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from cli_ec2_volume_snapshot import cli_ec2_volume_snapshot_init
    from cli_ec2_volume_snapshot import cli_ec2_volume_snapshot
    from ec2_volume import EC2VolumeManager
    from ec2_session import EC2SessionManager


def cli_ec2_volume_init():
    """Initialize awsbot cli for ec2 volume."""
    cli_ec2_volume_snapshot_init()
    cli_ec2_volume.add_command(cli_ec2_volume_snapshot)


@click.group('volume')
@cli_context
def cli_ec2_volume(session=None):
    """- AWS EC2 instance volumes Automation Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_volume.command('list')
@click.option('--instances', default=None,
              help='list volumes for the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='list volumes for all instances '
                   'for project tag:Project:<name>')
@cli_context
def list_volumes(session, instances, project_name):
    """List volumes associated with all instances."""
    aok, err = EC2VolumeManager(session.get_ec2_session()).\
        list_volumes(instances, project_name)

    if not aok:
        print(err)


if __name__ == '__main__':
    cli_ec2_volume_init()
    cli_ec2_volume()
