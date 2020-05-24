#!/bin/bash/evn python
# encoding=utf-8
"""
@file:getPathInfo.py
@time:5/24/20|11:39 PM
"""

import os


def get_path():
	"""os.path.split 将文件路径切割成头和尾的元祖 ，尾部总是最后一个斜线后面的部分"""
	path = os.path.split(os.path.realpath(__file__))[0]
	return path


if __name__ == '__main__':
	print(os.path.realpath(__file__))
	print(get_path())
