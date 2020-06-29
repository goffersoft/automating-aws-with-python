#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Python Packaging."""

from setuptools import setup

setup(
    name='awsbot-20',
    version='0.1',
    author='Goffer',
    author_email='goffersoft@gmail.com',
    description='awsbot 20 is a cli based automation tool/library for AWS',
    license='GPLv3+',
    packages=['awsbot'],
    package_data={
        "": ['resources/config/*',
             'resources/templates/policy/*',
             'resources/templates/www/*',
             'resources/templates/script/*'],
    },
    include_package_data=True,
    url='https://github.com/goffersoft/automating-aws-with-python',
    install_requires=['click',
                      'boto3',
                      'html5lib'],
    entry_points='''
        [console_scripts]
        awsbot=awsbot.awsbot:awsbot
    '''
)
