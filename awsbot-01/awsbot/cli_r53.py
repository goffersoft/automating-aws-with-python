#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for route53 awsbot commands."""

import click

try:
    from awsbot.r53_session import R53SessionManager
    from awsbot.r53_domain import R53DomainManager
    from awsbot.cli_globals import pass_context
except ImportError:
    from r53_session import R53SessionManager
    from r53_domain import R53DomainManager
    from cli_globals import pass_context


@click.group()
@pass_context
def r53(session):
    """- AWS Route 53 Automation Commands."""
    session.set_r53_session(R53SessionManager(session))


@r53.command('list-hosted-zones')
@pass_context
def list_hosted_zones(session):
    """List hosted zones."""
    R53DomainManager(session.get_r53_session()).\
        list_hosted_zones()


if __name__ == '__main__':
    pass
