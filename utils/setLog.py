#!/bin/bash/evn python
# encoding=utf-8
"""
@file:setLog.py
@time:5/24/20|11:53 PM
"""

import os
import logging
from getPathInfo import get_path
from logging.handlers import TimedRotatingFileHandler

path = get_path()
log_path = os.path.join(path, 'result')


class Logger(object):
	def __init__(self, log_name='logs|'):
		self.logger = logging.getLogger(log_name)
		logging.root.setLevel(logging.NOTSET)
		self.log_file_name = 'logs'
		self.backup_count = 5
		# output level
		self.console_output_level = 'WARNING'
		self.file_output_level = 'DEBUG'
		# output format
		self.formatter = logging.Formatter('%(asctime)s  %(name)s - %(levelname)s - %(message)s')

	def get_logger(self):
		""" check if there already exist a log handler if true just return"""
		if not self.logger.handlers:
			console_handler = logging.StreamHandler()
			console_handler.setFormatter(self.formatter)
			console_handler.setLevel(self.console_output_level)
			self.logger.addHandler(console_handler)
			# create a new log file everyday , max backup file is 5
			file_handler = TimedRotatingFileHandler(filename=os.path.join(log_path, self.log_file_name), when='D',
													interval=1, backupCount=self.backup_count, delay=True,
													encoding='utf-8')
			file_handler.setLevel(self.file_output_level)
			file_handler.setFormatter(self.formatter)
			self.logger.addHandler(file_handler)
			return self.logger


logger = Logger().get_logger()

if __name__ == '__main__':
	logger.debug('this is debug')
	logger.info('this is info')
	logger.warning('this is warning')
	logger.error('this is error')
