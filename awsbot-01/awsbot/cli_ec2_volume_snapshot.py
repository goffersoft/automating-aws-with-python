#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 volume snapshot Related CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_snapshot import EC2SnapshotManager
except ImportError:
    from cli_context import cli_context
    from ec2_snapshot import EC2SnapshotManager


@click.group('snapshot')
@cli_context
def ec2_volume_snapshot(session):
    """- AWS EC2 volume snapshots Automation Commands."""
    pass


@ec2_volume_snapshot.command('list')
@click.option('--instances', default=None,
              help='reboot the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='reboot all instances for project tag:Project:<name>')
@click.option('--all', 'list_all', default=False, is_flag=True,
              help='list all snapshots')
@cli_context
def list_volume_snapshots(session, instances, project_name, list_all):
    """List snapshots associated with all volumes."""
    ok, err = EC2SnapshotManager(session.get_ec2_session()).\
        list_volume_snapshots(instances, project_name, list_all)

    if not ok:
        print(err)


if __name__ == '__main__':
    pass
