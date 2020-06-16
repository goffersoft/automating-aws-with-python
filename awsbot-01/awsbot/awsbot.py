#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

try:
    from awsbot.cli_main import cli_init
    from awsbot.cli_main import cli
except ImportError:
    from cli_main import cli_init
    from cli_main import cli


def awsbot():
    """Initialize awsbot."""
    cli_init()
    cli()


if __name__ == '__main__':
    awsbot()
