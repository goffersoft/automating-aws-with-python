#! /usr/bin/python
# -*- coding:utf-8 -*-

"""ACM Certificate Manager class."""

from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


class ACMCertificateManager():
    """ACM Certificate Manager class."""

    cert_status_list = ('VALIDATION_TIMED_OUT',
                        'PENDING_VALIDATION',
                        'EXPIRED', 'INACTIVE',
                        'ISSUED', 'FAILED', 'REVOKED')

    def __init__(self, acm_session):
        """Initialize the acm certificate manager class."""
        self.acm_session = acm_session

    def cert_matches(self, cert_arn, domain_name):
        """Match domain to cert."""
        alt_names, err = self.get_cert_details(cert_arn,
                                               'SubjectAlternativeNames')
        if err:
            return False, err

        for name in alt_names:
            if name == domain_name:
                return True, None
            if name[0] == '*' and \
               domain_name.endswith(name[1:]):
                return True, None

        return False, None

    def get_cert_keys(self, cert_arn):
        """Get cert keys."""
        try:
            cert = self.acm_session.get_cert_details(cert_arn)
            if not cert:
                return None, \
                    f'Cannot find cert with this arn : {cert_arn}'
            return cert.get('Certificate').keys(), None
        except ClientError as client_error:
            return None, str(client_error)

    def get_cert_details(self, cert_arn, cert_filter=None):
        """Get cert details."""
        try:
            cert = self.acm_session.get_cert_details(cert_arn)
            if not cert:
                return None, \
                    f'Cannot find cert with this arn : {cert_arn}'
            return cert.get('Certificate').get(cert_filter, cert), None
        except ClientError as client_error:
            return None, str(client_error)

    def find_cert(self, domain_name):
        """Get cert that matches domain name."""
        try:
            for cert in self.acm_session.get_certs(['ISSUED']):
                aok, err = self.\
                    cert_matches(cert['CertificateArn'], domain_name)
                if err:
                    return None, err
                if aok:
                    return cert, None
            return None, \
                f'Cannot find cert matching : {domain_name}'
        except ClientError as client_error:
            return None, str(client_error)

    def list_certs(self, status_filter=None,
                   pfunc=lambda cert: print(cert)):
        """Print out a list of certs.

        Optionally filter by cert status
        """
        status = None
        err = None
        if status_filter:
            status, err = util.str_to_list(status_filter,
                                           self.cert_status_list)

        if err:
            return False, err

        try:
            for cert in self.acm_session.get_certs(status):
                pfunc(cert)
            return True, None
        except ClientError as client_error:
            return False, str(client_error)


if __name__ == '__main__':
    pass
