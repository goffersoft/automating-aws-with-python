#! /usr/bin.python
# -*- coding:utf-8 -*-

"""Boto3 s3 session context."""


class Boto3S3SessionContext():
    """S3 session context class."""

    def __init__(self, chunk_size=1024 * 1024 * 8):
        """Initialize Boto3 S3 Session Context."""
        self.chunk_size = chunk_size

    def get_chunk_size(self):
        """Get S3 transfer chunk size."""
        return self.chunk_size

    def set_chunk_size(self, chunk_size):
        """Set S3 transfer chunk size."""
        self.chunk_size = chunk_size


if __name__ == '__main__':
    pass
