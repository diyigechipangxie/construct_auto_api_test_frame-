#!/bin/bash/evn python
# encoding=utf-8
"""
@file:readConfig.py
@time:5/24/20|11:45 PM
"""
import os
from configparser import ConfigParser
from getPathInfo import get_path

path = get_path()
conf_path = os.path.join(path, 'config.ini')
conf_obj = ConfigParser()
conf_obj.read(conf_path, 'utf-8')


class ReadConf(object):
	def get_http(self, name):
		value = conf_obj.get('HTTP', name)
		return value

	def get_email(self, name):
		value = conf_obj.get('EMAIL', name)
		return value


if __name__ == '__main__':
	print(ReadConf().get_http('baseurl'))
	print(ReadConf().get_email('cc'))
