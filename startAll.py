#!/bin/bash/evn python
# encoding=utf-8
"""
@file:startAll.py
@time:5/25/20|3:51 PM
"""
import os
import unittest

from getPathInfo import get_path
from utils.setHTML import HTMLTestRunner
from utils.send_email import send_email
from readConfig import ReadConf
on_off = ReadConf().get_email('on_off')

path = get_path()

report_path = os.path.join(path, 'result')


class AllPatch(object):
	def __init__(self):
		global result_path
		result_path = os.path.join(report_path, 'report.html')
		self.caseListFile = os.path.join(path, 'caselist.txt')
		print(self.caseListFile)
		self.caseFile = os.path.join(path, 'testFile')
		print('self.caseFile{}'.format(self.caseFile))
		self.caseList = []

	def set_case_list(self):
		""" read case list from caselist.txt.txt"""
		fb = open(self.caseListFile)
		for data in fb.readlines():
			value = str(data)
			if value != '' and not value.startswith('#'):
				self.caseList.append(value.replace('\n', ''))
		print('caseList:{}'.format(self.caseList))
		fb.close()

	def set_case_suite(self):
		""" construct test suite """
		self.set_case_list()
		test_suite = unittest.TestSuite()
		suite_module = []
		for case in self.caseList:
			case_name = case.split('/')[-1]
			print(case_name + '.py')
			# load test
			discovered = unittest.defaultTestLoader.discover(self.caseFile, case_name + '.py', top_level_dir=None)
			suite_module.append(discovered)
			print('suite_module:', str(suite_module))

		if len(suite_module) > 0:
			for suite in suite_module:
				for suite_name in suite:
					test_suite.addTest(suite_name)
		else:
			print('set case suite else')
			return None

		return test_suite

	def run(self):
		try:
			suite = self.set_case_suite()
			print('try')
			print(str(suite))
			if suite:
				fp = open(result_path, 'wb')
				html_runner = HTMLTestRunner(stream=fp, title='test report', description='test login')
				html_runner.run(suite)
			else:
				print('failed, suite is None'.center(30, '*'))
		except Exception as e:
			print(str(e))

		finally:
			print('Test End'.center(30, '*'))

		if on_off == 'on':
			send_email()
		else:
			print('send email off . reopen it to send report.hmtl')


if __name__ == '__main__':
	AllPatch().run()