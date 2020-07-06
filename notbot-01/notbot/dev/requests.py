#!/usr/bin/python
# coding: utf-8
import requests
url='<your webhook url>'
data="{'text': 'Hello World'}"
requests.post(url, data)
