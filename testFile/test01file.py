#!/bin/bash/evn python
# encoding=utf-8
"""
@file:test01file.py
@time:5/24/20|10:34 PM
"""
import json
import unittest
import urllib.parse

import paramunittest

from getURL import get_url
from readExcel import ReadExcel
from utils.setHTTP import TestHTTP

rd = ReadExcel()
login_xls = rd.get_excel('loginCase.xlsx', 'login')
url = get_url()


@paramunittest.parametrized(*login_xls)
class TestLogin(unittest.TestCase):
	def setParameters(self, case_name, path, query, method):
		self.case_name = case_name
		self.path = path
		self.query = query
		self.method = method

	def description(self):
		self.case_name

	def setUp(self) -> None:
		print('before test')

	def test01login(self):
		self.check_result()

	def tearDown(self) -> None:
		print('after test')

	def check_result(self):
		url1 = 'http://www.xxxx.com/login?'
		new_url = url1 + self.query
		data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
		print('self.method', self.method)
		res = json.loads(TestHTTP().run(self.method, url, data1))
		if self.case_name == 'login':
			self.assertEqual(res['errcode'], 200)

		if self.case_name == 'login_error':
			self.assertEqual(res['errcode'], 1000)

		if self.case_name == 'login_null':
			self.assertEqual(res['errcode'], -1)



