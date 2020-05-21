#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for route53 awsbot commands."""

import click

try:
    from awsbot.r53_session import R53SessionManager
    from awsbot.cli_globals import pass_context
except ImportError:
    from r53_session import R53SessionManager
    from cli_globals import pass_context


@click.group()
@pass_context
def r53(session):
    """- AWS Route 53 Automation Commands."""
    session.set_r53_session(R53SessionManager(session))


if __name__ == '__main__':
    pass
