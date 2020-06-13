#! /usr/bin/python
# -*- coding:utf-8 -*-

"""S3 Bucket Manager class."""

from pathlib import Path


try:
    from awsbot import util
except ImportError:
    import util


class S3BucketManager():
    """S3 Bucket Manager class."""

    def __init__(self, s3_session):
        """Initialize BucketManager class."""
        self.s3_session = s3_session

    def list_buckets(self, pfunc=lambda bucket: print(bucket)):
        """List S3 Buckets Associated with this account."""
        for bucket in self.s3_session.get_s3_bucket_resources():
            pfunc(bucket)

    def list_bucket_objects(self, bucket_name,
                            pfunc=lambda object: print(object)):
        """List S3 Objects Associated with this S3 Bucket."""
        for obj in self.s3_session.\
                get_s3_bucket_resource(bucket_name).\
                objects.all():
            pfunc(obj)

    def setup_bucket(self, name, policy_file, index_file,
                     index_name, error_file, error_name):
        """Set up a bucket for web hosting.

        1) create a bucket using the (required) bucket name
        and policy as a json string or file
        default policy used if none provided
        2) add 2 html object to the bucket - index.html / error.html
        defaults used if none is provided
        3) enable web hosting on this bucket
        """
        bucket_res, err =\
            self.s3_session.create_s3_bucket(name, policy_file)
        if err is not None:
            self.s3_session.s3_bucket_cleanup(name, bucket_res)
            return None, f'Cannot create bucket {name}: {err}'

        aok, err = self.s3_session.\
            create_s3_bucket_object_html(bucket_res,
                                         index_file,
                                         index_name)
        if not aok:
            self.s3_session.s3_bucket_cleanup(name, bucket_res)
            return None, f'Cannot create bucket object {index_file} : {err}'

        aok, err = self.s3_session.\
            create_s3_bucket_object_html(bucket_res,
                                         error_file,
                                         error_name)
        if not aok:
            self.s3_session.s3_bucket_cleanup(name, bucket_res)
            return None, f'Cannot create bucket {error_file} : {err}'

        aok, err = self.s3_session.\
            s3_bucket_enable_webhosting(bucket_res,
                                        index_name,
                                        error_name)
        if not aok:
            self.s3_session.s3_bucket_cleanup(name, bucket_res)
            return None, f'Cannot enable web hosting{""}' +\
                         f' on bucket : {name} : {err}'

        return self.s3_session.get_s3_bucket_url(name)

    def sync_fs_to_bucket(self, fs_pathname, bucket_name, validate):
        """Sync fs to s3 bucket.

        sync files found in fs specified by 'fs_pathname' to bucket
        specified by 'bucket_name'.  optionally validate files (html only)
        """
        if not self.s3_session.is_valid_s3_bucket(bucket_name):
            return None, 'Bucket Doesnot Exist : ' + \
                          'Bucket needs to be setup first using ' + \
                          "the 'setup-bucket' command"

        path_map = {}
        err_map = {}
        metadata, _ =\
            self.s3_session.get_s3_object_metadata(bucket_name)

        def fswalk(path, root):
            pathname = str(path)
            filename = str(path.relative_to(root).as_posix())
            content_type = util.get_content_type_from_filename(filename)

            if validate and content_type.find('html') != -1:
                aok, err = util.is_valid_html_file(pathname)
                if not aok:
                    err_map[pathname] = err
                    return

            chunk_size = self.s3_session.get_chunk_size()
            sync_flag = True
            if metadata and metadata.get(filename, None):
                md5digest, err = util.md5digest(pathname, chunk_size)
                if not err and md5digest == metadata[filename][1:-1]:
                    sync_flag = False
            if sync_flag:
                path_map[pathname] = filename

        util.walk_fs_tree(Path(fs_pathname).expanduser().resolve(), fswalk)

        if len(err_map) == 0:
            for key, value in path_map.items():
                aok, err = \
                    self.s3_session.create_s3_bucket_object(
                        self.s3_session.get_s3_bucket_resource(bucket_name),
                        key, value)
                if not aok:
                    return None, err
            return self.s3_session.get_s3_bucket_url(bucket_name)

        return None, str(err_map)


if __name__ == '__main__':
    pass
