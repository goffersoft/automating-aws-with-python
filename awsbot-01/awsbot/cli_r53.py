#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for route53 awsbot commands."""

import click

try:
    from awsbot.r53_session import R53SessionManager
    from awsbot.r53_domain import R53DomainManager
    from awsbot.s3_session import S3SessionManager
    from awsbot.cli_context import cli_context
except ImportError:
    from r53_session import R53SessionManager
    from r53_domain import R53DomainManager
    from s3_session import S3SessionManager
    from cli_context import cli_context


def cli_r53_init():
    """Initialize awsbot cli for r53."""
    pass


@click.group('r53')
@cli_context
def cli_r53(session=None):
    """- AWS Route 53 Automation Commands."""
    session.set_r53_session(R53SessionManager(session))


@cli_r53.command('list-hosted-zones')
@cli_context
def list_hosted_zones(session):
    """List hosted zones."""
    R53DomainManager(session.get_r53_session()).\
        list_hosted_zones()


@cli_r53.command('list-record-sets')
@click.argument('zone', default=None)
@click.option('--type-filter', default=None,
              help='filter by record type')
@cli_context
def list_resource_record_sets(session, zone, type_filter):
    """List Resource Record Sets."""
    aok, err = R53DomainManager(session.get_r53_session()).\
        list_resource_record_sets(zone, type_filter)

    if not aok:
        print(str(err))


@cli_r53.command('setup-s3-domain')
@click.argument('bucket_name', default=None)
@cli_context
def setup_s3_domain(session, bucket_name):
    """Create S3 domain.

    The bucket should already exists in AWS S3
    (use the s3 cli commands to setup/sync s3 buckets)
    The bucket name is the domain name for S3 buckets
    The s3 bucket naming convention should be

    <bucketname>[.<sub-domain>].<registerd-domain>
    """
    helpdoc = """
                  Typically takes upto 10 minutes before
                  the url starts to work

                  if the hosted zone was also newly creted
                  as part of the domain setup and the url
                  doesnot work after 10 minutes or so,
                  then please read the following carefully
                  and act accordingly:

                      Before the Domain Name System will start
                      to route queries for this domain to Route 53
                      name servers, you must update the name server
                      records either with the current DNS service
                      or with the registrar for the domain,
                      as applicable.

               """

    domain_name = bucket_name

    s3_session = session.get_s3_session()
    if not s3_session:
        s3_session = S3SessionManager(session)

    bucket_region, err = s3_session.\
        get_region_name_from_s3_bucket(bucket_name)

    if err:
        print(err)
        return

    aok, err = R53DomainManager(session.get_r53_session()).\
        create_s3_domain_record(domain_name, bucket_region)

    if aok:
        print('Domain Creation Successful!')
        print()
        print(f's3 bucket url : http://{domain_name}')
        print(helpdoc)
    else:
        print(str(err))


if __name__ == '__main__':
    cli_r53_init()
    cli_r53()
