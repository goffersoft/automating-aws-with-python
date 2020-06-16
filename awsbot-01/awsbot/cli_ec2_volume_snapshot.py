#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 volume snapshot Related CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_snapshot import EC2SnapshotManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from ec2_snapshot import EC2SnapshotManager
    from ec2_session import EC2SessionManager


def cli_ec2_volume_snapshot_init():
    """Initialize awsbot cli for ec2 volume snapshots."""
    pass


@click.group('snapshot')
@cli_context
def cli_ec2_volume_snapshot(session=None):
    """- AWS EC2 volume snapshots Automation Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_volume_snapshot.command('list')
@click.option('--instances', default=None,
              help='list volume snapshots for the selected '
                   'instances (instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='list volume snapshots for all instances '
                   'for project tag:Project:<name>')
@click.option('--all', 'list_all', default=False, is_flag=True,
              help='list all volume snapshots (not just the latest ones')
@cli_context
def list_volume_snapshots(session, instances, project_name, list_all):
    """List snapshots associated with all volumes."""
    aok, err = EC2SnapshotManager(session.get_ec2_session()).\
        list_volume_snapshots(instances, project_name, list_all)

    if not aok:
        print(err)


@cli_ec2_volume_snapshot.command('create')
@click.option('--instances', default=None,
              help='create volume snapshots for the selected '
                   'instances (instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='create volume snapshots for all instances '
                   'for project tag:Project:<name>')
@click.option('--age', default=None, type=int,
              help='age value (in days) to determine if '
                   'volume snapshot can be created')
@cli_context
def create_volume_snapshots(session, instances, project_name, age):
    """Create volume snapshots associated with selected instances."""
    aok, err = EC2SnapshotManager(session.get_ec2_session()).\
        create_volume_snapshots(instances, project_name, age)

    if not aok:
        print(err)


if __name__ == '__main__':
    cli_ec2_volume_snapshot_init()
    cli_ec2_volume_snapshot()
