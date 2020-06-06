#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Key Pair Automation CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_keypair import EC2KeyPairManager
except ImportError:
    from cli_context import cli_context
    from ec2_keypair import EC2KeyPairManager


@click.group('keypair')
@cli_context
def ec2_keypair(session):
    """- AWS EC2 Key Pair Automation Commands."""
    pass


@ec2_keypair.command('list')
@cli_context
def list_keypair(session):
    """List All KeyPairs."""
    ok, err = EC2KeyPairManager(session.get_ec2_session()).\
        list_keypairs()

    if not ok:
        print(err)


@ec2_keypair.command('create')
@click.argument('name')
@click.argument('filename')
@cli_context
def create_keypair(session, name, filename):
    """Create KeyPair."""
    ok, err = EC2KeyPairManager(session.get_ec2_session()).\
        create_keypair(name, filename)

    if not ok:
        print(err)
        return

    print('KeyPair Successfully Created...')
    print(f'KeyPair Private Key (PEM Format) is in : {filename}')


@ec2_keypair.command('import')
@click.argument('name')
@click.argument('public-key')
@cli_context
def import_keypair(session, name, public_key):
    """Import KeyPair."""
    pass


@ec2_keypair.command('delete')
@click.argument('name')
@cli_context
def delete_keypair(session, name):
    """Delete KeyPair."""
    ok, err = EC2KeyPairManager(session.get_ec2_session()).\
        delete_keypair(name)

    if not ok:
        print(err)
        return

    print('KeyPair Successfully Deleted')


if __name__ == '__main__':
    pass
