#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

try:
    from awsbot.cli_main import cli
    from awsbot.cli_s3 import s3
    from awsbot.cli_r53 import r53
except ImportError:
    from cli_main import cli
    from cli_s3 import s3
    from cli_r53 import r53


def awsbot():
    """Initialize click cli.

    Add Sub-Commands to the main cli group
    """
    cli.add_command(s3)
    cli.add_command(r53)
    cli()


if __name__ == '__main__':
    awsbot()
