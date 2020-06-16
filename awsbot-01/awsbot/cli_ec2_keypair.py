#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Key Pair Automation CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_keypair import EC2KeyPairManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from ec2_keypair import EC2KeyPairManager
    from ec2_session import EC2SessionManager


def cli_ec2_keypair_init():
    """Initialize awsbot cli for ec2 keypairs."""
    pass


@click.group('keypair')
@cli_context
def cli_ec2_keypair(session=None):
    """- AWS EC2 Key Pair Automation Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_keypair.command('list')
@cli_context
def list_keypair(session):
    """List All KeyPairs."""
    aok, err = EC2KeyPairManager(session.get_ec2_session()).\
        list_keypairs()

    if not aok:
        print(err)


@cli_ec2_keypair.command('create')
@click.argument('keypair-name')
@click.argument('pem-filename')
@cli_context
def create_keypair(session, keypair_name, pem_filename):
    """Create KeyPair."""
    aok, err = EC2KeyPairManager(session.get_ec2_session()).\
        create_keypair(keypair_name, pem_filename)

    if not aok:
        print(err)
        return

    print('KeyPair Successfully Created...')
    print(f'KeyPair Private Key (PEM Format) is in : {pem_filename}')


@cli_ec2_keypair.command('import')
@click.argument('keypair-name')
@click.argument('public-key-file')
@cli_context
def import_keypair(session, keypair_name, public_key_file):
    """Import KeyPair."""
    aok, err = EC2KeyPairManager(session.get_ec2_session()).\
        import_keypair(keypair_name, public_key_file)

    if not aok:
        print(err)
        return

    print(f'KeyPair Successfully Imported From : {public_key_file}')


@cli_ec2_keypair.command('delete')
@click.argument('keypair-name')
@cli_context
def delete_keypair(session, keypair_name):
    """Delete KeyPair."""
    aok, err = EC2KeyPairManager(session.get_ec2_session()).\
        delete_keypair(keypair_name)

    if not aok:
        print(err)
        return

    print('KeyPair Successfully Deleted')


if __name__ == '__main__':
    cli_ec2_keypair_init()
    cli_ec2_keypair()
