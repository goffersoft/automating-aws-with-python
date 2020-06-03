#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for aws cloud front awsbot commands."""

import click

try:
    from awsbot.cf_session import CFSessionManager
    from awsbot.cf_distribution import CFDistributionManager
    from awsbot.s3_session import S3SessionManager
    from awsbot.r53_session import R53SessionManager
    from awsbot.r53_domain import R53DomainManager
    from awsbot.acm_session import ACMSessionManager
    from awsbot.acm_cert import ACMCertificateManager
    from awsbot.cli_context import cli_context
except ImportError:
    from cf_session import CFSessionManager
    from cf_distribution import CFDistributionManager
    from s3_session import S3SessionManager
    from r53_session import R53SessionManager
    from r53_domain import R53DomainManager
    from acm_session import ACMSessionManager
    from acm_cert import ACMCertificateManager
    from cli_context import cli_context


@click.group()
@cli_context
def cf(session):
    """- AWS Cloud Front Automation Commands."""
    session.set_cf_session(CFSessionManager(session))


@cf.command('list-all-distributions')
@cli_context
def list_all_distributions(session):
    """List all distributions."""
    err = CFDistributionManager(session.get_cf_session()).\
        list_all_distributions()

    if err:
        print(err)


@cf.command('list-distribution')
@click.argument('domain-name')
@cli_context
def list_distribution(session, domain_name):
    """List distribution matching domain name."""
    err = CFDistributionManager(session.get_cf_session()).\
        list_distribution(domain_name)

    if err:
        print(err)


@cf.command('setup-s3-cdn')
@click.argument('domain-name')
@click.option('--bucket-name', default=None,
              help='s3 bucket name (if different from domain-name)')
@click.option('--root-object', default='index.html',
              help='s3 cloud front distribution root object')
@click.option('--no-wait', default=False, is_flag=True,
              help='returns immediately instead of waiting for '
                   'the cloud front distribution to be deployed')
@cli_context
def setup_s3_cdn(session, domain_name, bucket_name, root_object, no_wait):
    """Create s3 cloud front distribution.

    1) Find distribution matching domain name - cf
    2) if the distribution is not found,
        a) find cert matching bucket name - acm
        b) get the bucket domain name
        c) create cdn distribution - cf
    4) create cf alias record - route 53
    """
    if not bucket_name:
        bucket_name = domain_name

    s3_session = session.get_s3_session()
    if not s3_session:
        s3_session = S3SessionManager(session)

    if not s3_session.is_valid_s3_bucket(bucket_name):
        print(f'S3 Bucket : {bucket_name} : Doesnot exist')
        return

    cert = None
    dist_manager = CFDistributionManager(session.get_cf_session())
    dist, err = dist_manager.find_distribution(domain_name)

    if err:
        acm_session = session.get_acm_session()
        if not acm_session:
            acm_session = ACMSessionManager(session)

        cert, err = ACMCertificateManager(acm_session).\
            find_cert(domain_name)
        if err:
            print(err)
            return

        s3_bucket_domain = f'{bucket_name}.s3.amazonaws.com'

        dist, err = dist_manager.\
            create_s3_distribution(domain_name, s3_bucket_domain,
                                   cert['CertificateArn'],
                                   root_object)
        if err:
            print(err)
            return

        if not no_wait:
            print('Waiting for distribution to be deployed...')

            _, err = dist_manager.\
                wait_for_distribution_to_be_deployed(dist['Id'])

            if err:
                print(err)
                return

    r53_session = session.get_r53_session()
    if not r53_session:
        r53_session = R53SessionManager(session)

    R53DomainManager(r53_session).\
        create_cf_domain_record(domain_name, dist['DomainName'])

    print()
    print(f'Domain Configured : https://{domain_name}')


if __name__ == '__main__':
    pass
