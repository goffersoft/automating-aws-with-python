#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Cloud Front Session Manager Class."""

try:
    from awsbot import util
except ImportError:
    import util


class CFSessionManager():
    """Cloud Front Session Manager Class."""

    def __init__(self, session):
        """Initialize the ACM Session Manager class."""
        self.session = session

    def get_cf_client(self):
        """Get cloud front client."""
        return self.session.get_client('cloudfront')

    def get_session(self):
        """Get session."""
        return self.session

    def set_session(self, session):
        """Set session."""
        self.session = session

    def get_cf_paginator(self, name):
        """Get cloud front paginator."""
        try:
            return self.get_cf_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_cf_list_distributions_paginator(self):
        """Get cloud front 'list_distributions' paginator."""
        return self.get_cf_paginator('list_distributions')[0]

    def get_distributions(self):
        """Iterate over distributions."""
        for page in self.\
                get_cf_list_distributions_paginator().\
                paginate():
            if page['DistributionList']['Quantity'] > 0:
                for item in page['DistributionList']['Items']:
                    yield item

    def get_cf_waiter(self, name):
        """Get cloud front waiter."""
        try:
            return self.get_cf_client().get_waiter(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_cf_distribution_deployed_waiter(self):
        """Get cloud front 'distribution_deployed' waiter."""
        return self.get_cf_waiter('distribution_deployed')[0]

    @staticmethod
    def create_cf_waiter_config(delay=30, max_attempts=50):
        """Create the json blob for cloud front waiter config."""
        return {'Delay': delay, 'MaxAttempts': max_attempts}

    @staticmethod
    def create_cf_distribution_config(domain_name, s3_bucket_domain, cert_arn,
                                      root_object='index.html',
                                      origin_id=None,
                                      comment_string='Created by AwsBot'):
        """Create the json blob for cloud front dist config."""
        if not origin_id:
            origin_id = f'S3-{domain_name}'

        return {'CallerReference': str(util.getuuid()),
                'Aliases': {
                    'Quantity': 1,
                    'Items': [
                        domain_name,
                    ]
                },
                'DefaultRootObject': root_object,
                'Comment': comment_string,
                'Enabled': True,
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': origin_id,
                        'DomainName': s3_bucket_domain,
                        'S3OriginConfig': {
                            'OriginAccessIdentity': ''
                        }}]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': origin_id,
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {
                            'Forward': 'all',
                        },
                        'Headers': {
                            'Quantity': 0,
                        },
                        'QueryStringCacheKeys': {
                            'Quantity': 0,
                        }
                    },
                    'TrustedSigners': {
                        'Quantity': 0,
                        'Enabled': False
                    },
                    'DefaultTTL': 86400,
                    'MinTTL': 3600,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                },
                'ViewerCertificate': {
                    'ACMCertificateArn': cert_arn,
                    'SSLSupportMethod': 'sni-only',
                    'MinimumProtocolVersion': 'TLSv1.1_2016'
                }}


if __name__ == '__main__':
    pass
