#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli globals."""

import click

try:
    from awsbot.session import SessionManager
except ImportError:
    from session import SessionManager


cli_context = click.make_pass_decorator(SessionManager,
                                         ensure=True)


if __name__ == '__main__':
    pass
