#!/bin/bash/evn python
# encoding=utf-8
"""
@file:readExcel.py
@time:5/24/20|11:37 PM
"""
import os

from xlrd import open_workbook
from getPathInfo import get_path

path = get_path()


class ReadExcel(object):

	def get_excel(self, xls_name, sheet_name):
		rows_ = []
		excel_path = os.path.join(path, 'testFile', 'caseDOC', xls_name)
		wb = open_workbook(excel_path)
		sheet = wb.sheet_by_name(sheet_name)
		nrows = sheet.nrows
		for i in range(nrows):
			if sheet.row_values(i)[0] != u'case_name':
				rows_.append(sheet.row_values(i))
		return rows_


if __name__ == '__main__':
	print(ReadExcel().get_excel('loginCase.xlsx', 'login'))
	print(ReadExcel().get_excel('loginCase.xlsx', 'login')[0][1])
	print(ReadExcel().get_excel('loginCase.xlsx', 'login')[1][2])