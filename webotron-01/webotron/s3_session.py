#! /usr/bin.python
# -*- coding:utf-8 -*-

"""s3 session manager class."""

from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig

try:
    import util
except ModuleNotFoundError:
    from . import util


class S3SessionManager():
    """S3 session context class."""

    def __init__(self, session, chunk_size=1024 * 1024 * 8):
        """Initialize S3 Session Manager."""
        self.session = session
        self.chunk_size = chunk_size

    def get_chunk_size(self):
        """Get S3 transfer chunk size."""
        return self.chunk_size

    def set_chunk_size(self, chunk_size):
        """Set S3 transfer chunk size."""
        self.chunk_size = chunk_size

    def get_session(self):
        """Get session."""
        return self.session

    def set_session(self, session):
        """Set session."""
        self.session = session

    def get_s3_resource(self):
        """Get s3 resource."""
        return self.session.get_resource('s3')

    def get_s3_client(self):
        """Get s3 client."""
        return self.session.get_client('s3')

    def get_s3_bucket_resources(self):
        """Get all s3 bucket resources as iterable."""
        return self.get_s3_resource().buckets.all()

    def get_s3_bucket_resource(self, name):
        """Get s3 bucket resource associated with name."""
        return self.get_s3_resource().Bucket(name)

    def get_s3_paginator(self, name):
        """Get s3 paginator."""
        try:
            return self.get_s3_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_s3_list_bucket_v2_paginator(self):
        """Get s3 'ListObjectsV2' paginator."""
        return self.get_s3_paginator('list_objects_v2')[0]

    def is_valid_s3_bucket(self, name):
        """Validate s3 bucket.

        check to see if bucket associated with 'name'
         has been created or not
        """
        return self.get_s3_bucket_resource(name).creation_date is not None

    def s3_bucket_cleanup(self, bucket_name, bucket_res):
        """Delete S3 bucket and associated contents."""
        pass

    def create_s3_bucket_policy(self, bucket_res, policy, validate=True):
        """Create and associate a policy with this 33 bucket."""
        if validate:
            policy, err =\
                self.validate_and_get_s3_bucket_policy_as_string(
                    bucket_res.name, policy)

            if err is not None:
                return False, err

        try:
            self.get_s3_bucket_policy_resource(bucket_res).put(Policy=policy)
            return True, None
        except ClientError as client_error:
            return False, str(client_error)

    def validate_and_get_s3_bucket_policy_as_string(self,
                                                    bucket_name,
                                                    bucket_policy):
        """Validate S3 bucket policy.

        validates the s3 bucket policy (file or a string)
        and return the s3 bucket policy as string
        """
        ok, file_type, err = self.is_valid_s3_bucket_policy(bucket_policy)

        if not ok:
            return None, err

        if file_type == 'file':
            bucket_policy, err = util.get_file_as_string(bucket_policy)
            if err is not None:
                return None, err

        return bucket_policy % bucket_name, None

    def get_region_name_from_s3_bucket(self, bucket_name):
        """Get S3 bucket region_name from bucket name."""
        try:
            response_dict = self.get_s3_resource().\
                            meta.client.\
                            get_bucket_location(Bucket=bucket_name)
            return response_dict['LocationConstraint'] or \
                self.session.get_default_region()
        except ClientError as client_error:
            return None, str(client_error)

    def get_s3_bucket_url(self, bucket_name):
        """Get S3 bucket url."""
        try:
            region_name = self.get_region_name_from_s3_bucket(bucket_name)
            endpoint, err = self.session.get_region_config().\
                get_endpoint(region_name)
            if err:
                return None, err
            return f'http://{bucket_name}.{endpoint}', None
        except ClientError as client_error:
            return None, str(client_error)

    def create_s3_bucket_object_html(self, bucket_res,
                                     html_content, keyname):
        """Create a s3 bucket (html) object."""
        ok, file_type, err = util.is_valid_html(html_content)

        if not ok:
            return False, err

        try:
            if file_type == 'str':
                self.get_s3_resource()\
                                 .Object(bucket_res.name, keyname)\
                                 .put(Body=bytes(html_content),
                                      ContentType='text/html')
                return True, None

            return self.create_s3_bucket_object(bucket_res,
                                                html_content, keyname,
                                                'text/html')
        except ClientError as client_error:
            return False, str(client_error)

    def create_s3_bucket_object(self, bucket_res,
                                filename, keyname,
                                content_type=None):
        """Create a s3 object in the specified bucket."""
        try:
            if content_type is None:
                content_type = util.get_content_type_from_filename(keyname)

            chunk_size = self.session.get_s3_session().get_chunk_size()
            filename, err = util.get_file_path(filename)
            if err:
                return False, err
            bucket_res.upload_file(
                filename, keyname,
                ExtraArgs={'ContentType': content_type},
                Config=TransferConfig(
                    multipart_threshold=chunk_size,
                    multipart_chunksize=chunk_size))
        except ClientError as client_error:
            return False, str(client_error)

        return True, None

    def get_s3_object_metadata(self, bucket_name):
        """Get etag associated with S3 objects."""
        paginator = self.get_s3_list_bucket_v2_paginator()

        metadata = {}

        try:
            pages = paginator.paginate(Bucket=bucket_name)
            for page in pages:
                for meta in page['Contents']:
                    metadata[meta['Key']] = meta['ETag']
            return metadata, None
        except ClientError as client_error:
            return None, str(client_error)

    def create_s3_bucket(self, name, policy):
        """Create a s3 bucket."""
        bucket = None

        try:
            policy, err = \
                self.validate_and_get_s3_bucket_policy_as_string(name, policy)

            if err is not None:
                return None, err

            bucket_region = self.session.get_region_name()

            if self.is_valid_s3_bucket(name):
                bucket_region =\
                    self.get_region_name_from_s3_bucket(name)

            if self.session.is_default_region(bucket_region):
                bucket =\
                    self.get_s3_resource().create_bucket(Bucket=name)
            else:
                bucket = self.get_s3_resource()\
                    .create_bucket(Bucket=name,
                                   CreateBucketConfiguration={
                                       'LocationConstraint':
                                       bucket_region})

            ok, err = self.create_s3_bucket_policy(bucket, policy, False)

            if not ok:
                return None, f'Fatal : Cannot Create Bucket Policy : {err}'

        except ClientError as client_error:
            if self.session.get_client_error_code(client_error) == \
               'BucketAlreadyOwnedByYou':
                bucket = self.get_s3_bucket_resource(name)
            else:
                return None, str(client_error)

        return bucket, None

    @staticmethod
    def get_s3_bucket_website_resource(bucket_resource):
        """Get s3 website resource associated with this bucket resource."""
        return bucket_resource.Website()

    @staticmethod
    def get_s3_bucket_policy_resource(bucket_resource):
        """Get s3 policy resource associated with this bucket resource."""
        return bucket_resource.Policy()

    @staticmethod
    def is_valid_s3_bucket_policy(policy):
        """Validdate the policy file or the policy string passed in."""
        return util.is_valid_json(policy)

    @staticmethod
    def is_valid_s3_bucket_object_html(html):
        """Validdate the bucket object as a valid html file or a string."""
        return util.is_valid_html(html)

    @staticmethod
    def s3_bucket_enable_webhosting(bucket_res, index_name, error_name):
        """Enable web hosting on this bucket."""
        try:
            web = S3SessionManager.\
                get_s3_bucket_website_resource(bucket_res)

            web.put(WebsiteConfiguration={
                'IndexDocument': {'Suffix': index_name},
                'ErrorDocument': {'Key': error_name}, })

            return True, None
        except ClientError as client_error:
            return False, str(client_error)


if __name__ == '__main__':
    pass
