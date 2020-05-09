from boto3_helper import *
from util import *

g_s3_bucket_url_template = 'http://%s.s3-website-%s.amazonaws.com'


def get_s3_resource():
    """ get s3 resource """

    return get_resource('s3')


def get_s3_client():
    """ get s3 client """

    return get_client('s3')


def get_s3_bucket_resources():
    """ get all s3 bucket resources as iterable """

    return get_s3_resource().buckets.all()


def get_s3_bucket_resource(name):
    """ get s3 bucket resource associated with name """

    return get_s3_resource().Bucket(name)


def get_s3_bucket_website_resource(bucket_resource):
    """ get s3 website resource associated with this bucket resource """

    return bucket_resource.Website()


def get_s3_bucket_policy_resource(bucket_resource):
    """ get s3 policy resource associated with this bucket resource """

    return bucket_resource.Policy()


def is_valid_s3_bucket_policy(policy):
    """ validdate the policy file or the policy string passed in """

    return is_valid_json(policy)


def is_valid_s3_bucket_object_html(html):
    """ validdate the bucket object as a valid html file or a string """

    return is_valid_html(html)


def s3_bucket_enable_webhosting(bucket_res, index_name, error_name):
    """ enbale web hosting on this bucket """

    try:
        web = get_s3_bucket_website_resource(bucket_res)

        web.put(WebsiteConfiguration={
                'IndexDocument': {'Suffix': index_name},
                'ErrorDocument': {'Key': error_name}, })

        return True, None
    except ClientError as e:
        return False, str(e)


def s3_bucket_cleanup(bucket_res):
    pass


def create_s3_bucket_policy(bucket_res, policy, validate=True):
    """ create/associate a policy with this 33 bucket """

    if validate:
        policy, err =\
            validate_and_get_s3_bucket_policy_as_string(
                bucket_res.name, policy)

        if err is not None:
            return False, err

    try:
        get_s3_bucket_policy_resource(bucket_res).put(Policy=policy)
        return True, None
    except ClientError as e:
        return False, str(e)


def validate_and_get_s3_bucket_policy_as_string(bucket_name, bucket_policy):
    """ validates the s3 bucket policy (file or a string)
        and return the s3 bucket policy as string
    """

    ok, type, err = is_valid_s3_bucket_policy(bucket_policy)

    if not ok:
        return None, err

    if type == 'file':
        bucket_policy, err = get_file_as_string(bucket_policy)
        if err is not None:
            return None, err

    return bucket_policy % bucket_name, None


def get_s3_bucket_url(bucket_name):
    return g_s3_bucket_url_template % (bucket_name, get_session().region_name)


def create_s3_bucket(name, policy):
    """ create a s3 bucket """

    bucket = None

    try:
        policy, err = \
            validate_and_get_s3_bucket_policy_as_string(name, policy)

        if err is not None:
            return None, err

        if is_default_region():
            bucket = get_s3_resource().create_bucket(Bucket=name)
        else:
            bucket = get_s3_resource()\
                .create_bucket(Bucket=name,
                               CreateBucketConfiguration={
                                   'LocationConstraint':
                                   get_session().region_name})

        ok, err = create_s3_bucket_policy(bucket, policy, False)

        if not ok:
            return None, f'Fatal : Cannot Create Bucket Policy : {err}'

    except ClientError as e:
        if getClientErrorCode(e) == 'BucketAlreadyOwnedByYou':
            bucket = get_s3_bucket_resource(name)
        else:
            return None, str(e)

    return bucket, None


def create_s3_bucket_object_html(bucket_res, html, filename):
    """ create a s3 bucket (html) object """

    ok, type, err = is_valid_html(html)

    if not ok:
        return False, err

    try:
        if type == 'str':
            get_s3_resource().Object(bucket_res.name, filename)\
                             .put(Body=bytes(html),
                                  ontentType='text/html')
        else:
            bucket_res.upload_file(html, filename,
                                   ExtraArgs={'ContentType': 'text/html'})
    except ClientError as e:
        return False, str(e)

    return True, None


if __name__ == '__main__':
    pass