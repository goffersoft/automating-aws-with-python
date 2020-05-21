#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

try:
    from awsbot.awsbots3cli import s3
    from awsbot.awsbotmaincli import cli
except ImportError:
    from awsbots3cli import s3
    from awsbotmaincli import cli


def awsbot():
    """Initialize click cli.

    Add Sub-Commands to the main cli group
    """
    cli.add_command(s3)
    cli()


if __name__ == '__main__':
    awsbot()
