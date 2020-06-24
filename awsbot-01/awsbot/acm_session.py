#! /usr/bin/python
# -*- coding:utf-8 -*-

"""ACM Session Manager Class."""


class ACMSessionManager():
    """AWS Cert. Session Manager Class."""

    def __init__(self, session):
        """Initialize the ACM Session Manager class."""
        self.session = session

    def get_acm_client(self):
        """Get acm client."""
        return self.session.get_client('acm')

    def get_session(self):
        """Get session."""
        return self.session

    def set_session(self, session):
        """Set session."""
        self.session = session

    def get_acm_paginator(self, name):
        """Get acm paginator."""
        try:
            return self.get_acm_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_acm_list_certificates_paginator(self):
        """Get acm 'list_certificates' paginator."""
        return self.get_acm_paginator('list_certificates')[0]

    def get_certs(self, cert_status_list):
        """Iterate over certificates."""
        paginator = self.get_acm_list_certificates_paginator()
        if cert_status_list:
            pages = paginator.\
                paginate(CertificateStatuses=cert_status_list)
        else:
            pages = paginator.paginate()

        for page in pages:
            for cert in page['CertificateSummaryList']:
                yield cert

    def get_cert_details(self, cert_arn):
        """Get cert details."""
        return self.get_acm_client().\
            describe_certificate(CertificateArn=cert_arn)


if __name__ == '__main__':
    pass
