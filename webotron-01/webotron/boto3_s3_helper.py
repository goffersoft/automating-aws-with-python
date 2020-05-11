#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Boto3 S3 helper functions."""

from pathlib import Path

from botocore.exceptions import ClientError

import boto3_helper
import util
import region_util


def get_s3_resource():
    """Get s3 resource."""
    return boto3_helper.get_resource('s3')


def get_s3_client():
    """Get s3 client."""
    return boto3_helper.get_client('s3')


def get_s3_bucket_resources():
    """Get all s3 bucket resources as iterable."""
    return get_s3_resource().buckets.all()


def get_s3_bucket_resource(name):
    """Get s3 bucket resource associated with name."""
    return get_s3_resource().Bucket(name)


def is_valid_s3_bucket(name):
    """Validate s3 bucket.

    check to see if bucket associated with 'name'.  has been created or not
    """
    return get_s3_bucket_resource(name).creation_date is not None


def get_s3_bucket_website_resource(bucket_resource):
    """Get s3 website resource associated with this bucket resource."""
    return bucket_resource.Website()


def get_s3_bucket_policy_resource(bucket_resource):
    """Get s3 policy resource associated with this bucket resource."""
    return bucket_resource.Policy()


def is_valid_s3_bucket_policy(policy):
    """Validdate the policy file or the policy string passed in."""
    return util.is_valid_json(policy)


def is_valid_s3_bucket_object_html(html):
    """Validdate the bucket object as a valid html file or a string."""
    return util.is_valid_html(html)


def s3_bucket_enable_webhosting(bucket_res, index_name, error_name):
    """Enable web hosting on this bucket."""
    try:
        web = get_s3_bucket_website_resource(bucket_res)

        web.put(WebsiteConfiguration={
            'IndexDocument': {'Suffix': index_name},
            'ErrorDocument': {'Key': error_name}, })

        return True, None
    except ClientError as client_error:
        return False, str(client_error)


def s3_bucket_cleanup(bucket_name, bucket_res):
    """Delete S3 bucket and associated contents."""
    pass


def create_s3_bucket_policy(bucket_res, policy, validate=True):
    """Create and associate a policy with this 33 bucket."""
    if validate:
        policy, err =\
            validate_and_get_s3_bucket_policy_as_string(
                bucket_res.name, policy)

        if err is not None:
            return False, err

    try:
        get_s3_bucket_policy_resource(bucket_res).put(Policy=policy)
        return True, None
    except ClientError as client_error:
        return False, str(client_error)


def validate_and_get_s3_bucket_policy_as_string(bucket_name, bucket_policy):
    """Validate S3 bucket policy.

    validates the s3 bucket policy (file or a string)
    and return the s3 bucket policy as string
    """
    ok, file_type, err = is_valid_s3_bucket_policy(bucket_policy)

    if not ok:
        return None, err

    if file_type == 'file':
        bucket_policy, err = util.get_file_as_string(bucket_policy)
        if err is not None:
            return None, err

    return bucket_policy % bucket_name, None


def get_s3_bucket_url(bucket_name):
    """Get S3 bucket url."""
    endpoint = region_util.get_endpoint(boto3_helper.get_session().region_name)
    return f'http://{bucket_name}.{endpoint}'


def create_s3_bucket(name, policy):
    """Create a s3 bucket."""
    bucket = None

    try:
        policy, err = \
            validate_and_get_s3_bucket_policy_as_string(name, policy)

        if err is not None:
            return None, err

        if boto3_helper.is_default_region():
            bucket = get_s3_resource().create_bucket(Bucket=name)
        else:
            bucket = get_s3_resource()\
                .create_bucket(Bucket=name,
                               CreateBucketConfiguration={
                                   'LocationConstraint':
                                   boto3_helper.get_session().region_name})

        ok, err = create_s3_bucket_policy(bucket, policy, False)

        if not ok:
            return None, f'Fatal : Cannot Create Bucket Policy : {err}'

    except ClientError as client_error:
        if boto3_helper.get_client_error_code(client_error) == \
           'BucketAlreadyOwnedByYou':
            bucket = get_s3_bucket_resource(name)
        else:
            return None, str(client_error)

    return bucket, None


def create_s3_bucket_object_html(bucket_res, html_content, keyname):
    """Create a s3 bucket (html) object."""
    ok, file_type, err = util.is_valid_html(html_content)

    if not ok:
        return False, err

    try:
        if file_type == 'str':
            get_s3_resource().Object(bucket_res.name, keyname)\
                             .put(Body=bytes(html_content),
                                  ContentType='text/html')
        else:
            bucket_res.upload_file(html_content, keyname,
                                   ExtraArgs={'ContentType': 'text/html'})
    except ClientError as client_error:
        return False, str(client_error)

    return True, None


def create_s3_bucket_object(bucket_res,
                            filename, keyname,
                            content_type=None):
    """Create a s3 object in the specified bucket."""
    try:
        if content_type is None:
            content_type = util.get_content_type_from_filename(keyname)

        bucket_res.upload_file(filename, keyname,
                               ExtraArgs={'ContentType': content_type})
    except ClientError as client_error:
        return False, str(client_error)

    return True, None


def setup_s3_bucket(name, policy_file, index_file,
                    index_name, error_file, error_name):
    """Set up a bucket for web hosting.

    1) create a bucket using the (required) bucket name
    and policy as a json string or file
    default policy used if none provided
    2) add 2 html object to the bucket - index.html / error.html
    defaults used if none is provided
    3) enable web hosting on this bucket
    """
    bucket_res, err = create_s3_bucket(name, policy_file)
    if err is not None:
        s3_bucket_cleanup(name, bucket_res)
        return None, f'Cannot create bucket {name}: {err}'

    ok, err = create_s3_bucket_object_html(bucket_res,
                                           index_file,
                                           index_name)
    if not ok:
        s3_bucket_cleanup(name, bucket_res)
        return None, f'Cannot create bucket object {index_file} : {err}'

    ok, err = create_s3_bucket_object_html(bucket_res,
                                           error_file,
                                           error_name)
    if not ok:
        s3_bucket_cleanup(name, bucket_res)
        return None, f'Cannot create bucket {error_file} : {err}'

    ok, err = s3_bucket_enable_webhosting(bucket_res,
                                          index_name,
                                          error_name)
    if not ok:
        s3_bucket_cleanup(name, bucket_res)
        return None, f'Cannot enable web hosting on bucket : {name} : {err}'

    return get_s3_bucket_url(name), None


def sync_fs_to_s3_bucket(fs_pathname, bucket_name, validate):
    """Sync fs to s3 bucket.

    sync files found in fs specified by 'fs_pathname' to bucket
    specified by 'bucket_name'.  optionally validate files (html only)
    """
    if not is_valid_s3_bucket(bucket_name):
        return False, 'Bucket Doesnot Exist : ' + \
                      'Bucket needs to be setup first using ' + \
                      "the 'setup-bucket' command"

    path_map = {}
    err_map = {}

    def fswalk(p, root):
        pathname = str(p)
        filename = str(p.relative_to(root).as_posix())
        content_type = util.get_content_type_from_filename(filename)

        if validate and content_type.find('html') != -1:
            ok, err = util.is_valid_html_file(pathname)
            if not ok:
                err_map[pathname] = err
                return

        path_map[pathname] = filename

    util.walk_fs_tree(Path(fs_pathname).expanduser().resolve(), fswalk)

    if len(err_map) == 0:
        for k, v in path_map.items():
            ok, err = \
                create_s3_bucket_object(
                    get_s3_bucket_resource(bucket_name), k, v)
            if not ok:
                return False, err
        return True, None

    return False, str(err_map)


if __name__ == '__main__':
    pass
