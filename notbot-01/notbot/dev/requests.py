#!/usr/bin/python
# coding: utf-8
import requests
url='https://hooks.slack.com/services/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'
data="{'text': 'Hello World'}"
requests.post(url, data)
