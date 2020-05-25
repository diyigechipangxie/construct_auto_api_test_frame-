#!/bin/bash/evn python
# encoding=utf-8
"""
@file:getURL.py
@time:5/25/20|12:54 AM
"""
from readConfig import ReadConf


def get_url():
	rd = ReadConf()
	protocol = rd.get_http('scheme')
	baseurl = rd.get_http('baseurl')
	port = rd.get_http('port')
	return protocol + '://' + baseurl + ':' + port + '/login?'


if __name__ == '__main__':
	print(get_url())
