#! /usr/bin/python
# -*- coding:utf-8 -*-

"""cli entry points for aws cert manager awsbot commands."""

import click

try:
    from awsbot.acm_session import ACMSessionManager
    from awsbot.acm_cert import ACMCertificateManager
    from awsbot.cli_context import cli_context
except ImportError:
    from acm_session import ACMSessionManager
    from acm_cert import ACMCertificateManager
    from cli_context import cli_context


@click.group()
@cli_context
def acm(session):
    """- AWS ACM Automation Commands."""
    session.set_acm_session(ACMSessionManager(session))


@acm.command('find-cert')
@click.argument('domain-name')
@cli_context
def find_cert(session, domain_name):
    """Find cert that matches domain name."""
    cert, err = ACMCertificateManager(session.get_acm_session()).\
        find_cert(domain_name)

    if err:
        print(err)
    else:
        print(cert)


@acm.command('list-certs')
@click.option('--status-filter', default='ISSUED',
              help='filter by certificate status. '
              'status can be one or more of '
              '(separated by commas) '
              'VALIDATION_TIMED_OUT, '
              'PENDING_VALIDATION, '
              'EXPIRED, INACTIVE, '
              'ISSUED, FAILED, REVOKED')
@cli_context
def list_certs(session, status_filter):
    """List certs.

    Optionally filter by cert. status
    status can be one or more of (separated by commas)
    VALIDATION_TIMED_OUT, PENDING_VALIDATION, EXPIRED,
    INACTIVE, ISSUED, FAILED, REVOKED
    """
    ok, err = ACMCertificateManager(session.get_acm_session()).\
        list_certs(status_filter)

    if not ok:
        print(err)


@acm.command('list-cert-keys')
@click.argument('cert-arn')
@cli_context
def list_cert_keys(session, cert_arn):
    """Get cert keys."""
    cert_keys, err = ACMCertificateManager(session.get_acm_session()).\
        get_cert_keys(cert_arn)

    if err:
        print(err)
    else:
        for i, key in enumerate(cert_keys):
            print(f'{i+1:>2} : {key}')


@acm.command('get-cert-details')
@click.argument('cert-arn')
@click.option('--cert-filter', default=None,
              help='filter by any primary key '
              'in the returned json blob '
              'describing the cert')
@cli_context
def get_cert_details(session, cert_arn, cert_filter):
    """Get cert details.

    optionally, fiter by any key in the json
    blob describing the cert.
    """
    cert, err = ACMCertificateManager(session.get_acm_session()).\
        get_cert_details(cert_arn, cert_filter)

    if err:
        print(err)
    else:
        print(cert)


if __name__ == '__main__':
    pass
