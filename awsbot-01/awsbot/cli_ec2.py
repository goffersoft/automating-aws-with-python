#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from ec2_session import EC2SessionManager


@click.group()
@cli_context
def ec2(session):
    """- AWS EC2 Automation Commands."""
    session.set_ec2_session(EC2SessionManager(session))


if __name__ == '__main__':
    pass
