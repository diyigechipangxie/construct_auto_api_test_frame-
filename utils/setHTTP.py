#!/bin/bash/evn python
# encoding=utf-8
"""
@file:setHTTP.py
@time:5/24/20|11:53 PM
"""
import json

import requests


class TestHTTP(object):

	def send_get(self, url, data):
		""" .json() 返回json对象的响应"""
		resp = requests.get(url, params=data).json()
		res = json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=2)
		return res

	def send_post(self, url, data):
		resp = requests.post(url, data=data).json()
		res = json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=2)
		return res

	def run(self, method, url, data):
		res = None
		if method == 'GET':
			res = self.send_get(url, data)
		elif method == "POST":
			res = self.send_post(url, data)
		else:
			print('method not allowed')
		return res

