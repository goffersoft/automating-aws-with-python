#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for route53 awsbot commands."""

import click

try:
    from awsbot.r53_session import R53SessionManager
    from awsbot.r53_domain import R53DomainManager
    from awsbot.s3_session import S3SessionManager
    from awsbot.cli_globals import pass_context
except ImportError:
    from r53_session import R53SessionManager
    from r53_domain import R53DomainManager
    from s3_session import S3SessionManager
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


@r53.command('list-record-sets')
@click.argument('zone', default=None)
@click.option('--type-filter', default=None,
              help='filter by record type')
@pass_context
def list_resource_record_sets(session, zone, type_filter):
    """List Resource Record Sets."""
    ok, err = R53DomainManager(session.get_r53_session()).\
        list_resource_record_sets(zone, type_filter)

    if not ok:
        print(str(err))


@r53.command('setup-s3-domain')
@click.argument('domain_name', default=None)
@pass_context
def setup_s3_domain(session, domain_name):
    """Create S3 domain."""
    bucket_name = domain_name

    if session.get_s3_session():
        s3_session = session.get_s3_session()
    else:
        s3_session = S3SessionManager(session)

    bucket_region, err = s3_session.\
        get_region_name_from_s3_bucket(bucket_name)

    if err:
        print(err)
        return

    ok, err = R53DomainManager(session.get_r53_session()).\
        create_s3_domain_record(domain_name, bucket_region)

    if ok:
        print(f'Successfully created S3 Domain for bucket : {domain_name}')
    else:
        print(str(err))


if __name__ == '__main__':
    pass
