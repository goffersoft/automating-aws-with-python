#! /usr/bin/python
# -*- coding:utf-8 -*-

"""CloudWatch cli commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.cw_session import CWSessionManager
    from awsbot.cli_cw_alarm import cli_cw_alarm
    from awsbot.cli_cw_alarm import cli_cw_alarm_init
except ImportError:
    from cli_context import cli_context
    from cw_session import CWSessionManager
    from cli_cw_alarm import cli_cw_alarm
    from cli_cw_alarm import cli_cw_alarm_init


def cli_cw_init():
    """Initialize cloud watch cli."""
    cli_cw_alarm_init()
    cli_cw.add_command(cli_cw_alarm)


@click.group('cw')
@cli_context
def cli_cw(session=None):
    """- AWS Cloudwatch Automation Commands."""
    session.set_cw_session(CWSessionManager(session))


if __name__ == '__main__':
    cli_cw_init()
    cli_cw()
