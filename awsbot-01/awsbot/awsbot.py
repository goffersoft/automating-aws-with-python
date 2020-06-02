#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for the various awsbot commands."""

try:
    from awsbot.cli_main import cli
    from awsbot.cli_s3 import s3
    from awsbot.cli_r53 import r53
    from awsbot.cli_acm import acm
    from awsbot.cli_cf import cf
    from awsbot.cli_ec2 import ec2
    from awsbot.cli_ec2_instance import ec2_instance
except ImportError:
    from cli_main import cli
    from cli_s3 import s3
    from cli_r53 import r53
    from cli_acm import acm
    from cli_cf import cf
    from cli_ec2 import ec2
    from cli_ec2_instance import ec2_instance


def cli_init_s3():
    """Initialize awsbot cli for s3."""
    cli.add_command(s3)


def cli_init_r53():
    """Initialize awsbot cli for r53."""
    cli.add_command(r53)


def cli_init_acm():
    """Initialize awsbot cli for acm."""
    cli.add_command(acm)


def cli_init_cf():
    """Initialize awsbot cli for cf."""
    cli.add_command(cf)


def cli_init_ec2():
    """Initialize awsbot cli for ec2."""
    ec2.add_command(ec2_instance)
    cli.add_command(ec2)


def awsbot():
    """Initialize awsbot.

    Configure click package
    Add Sub-Commands to the main cli group
    """
    cli_init_s3()
    cli_init_r53()
    cli_init_acm()
    cli_init_cf()
    cli_init_ec2()
    cli()


if __name__ == '__main__':
    awsbot()
