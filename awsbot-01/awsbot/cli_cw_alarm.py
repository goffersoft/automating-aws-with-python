#! /usr/bin/python
# -*- coding:utf-8 -*-

"""CloudWatch alarms cli commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.cw_session import CWSessionManager
    from awsbot.cw_alarm import CWAlarmManager
except ImportError:
    from cli_context import cli_context
    from cw_session import CWSessionManager
    from cw_alarm import CWAlarmManager


def cli_cw_alarm_init():
    """Initialize cloud watch alarms cli commands."""
    pass


@click.group('alarm')
@cli_context
def cli_cw_alarm(session=None):
    """- CloudWatch alarm cli commands."""
    if not session.get_cw_session():
        session.set_cw_session(CWSessionManager(session))


@cli_cw_alarm.command('list')
@click.option('--metric-alarms/--composite-alarms', default=None,
              help='print alarm detais')
@click.option('--long', is_flag=True,
              help='print alarm detais')
@cli_context
def list_alarms(session, metric_alarms, long):
    """List cloudwatch alarms."""
    cw_alarm_mgr = CWAlarmManager(session.get_cw_session())

    err = None
    err1 = None

    if metric_alarms is None:
        _, err = cw_alarm_mgr.list_metric_alarms(long_version=long)
        _, err1 = cw_alarm_mgr.list_composite_alarms(long_version=long)
    elif metric_alarms:
        _, err = cw_alarm_mgr.list_metric_alarms(long_version=long)
    else:
        _, err1 = cw_alarm_mgr.list_composite_alarms(long_version=long)

    if err:
        print(err)

    if err1:
        print(err)


if __name__ == '__main__':
    cli_cw_alarm_init()
    cli_cw_alarm()
