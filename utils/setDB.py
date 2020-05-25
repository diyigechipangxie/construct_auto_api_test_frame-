#!/bin/bash/evn python
# encoding=utf-8
"""
@file:setDB.py
@time:5/24/20|11:52 PM
"""
import os
from datetime import datetime, timedelta, date

from pymysql.connections import Connection
import pymysql.err
from readConfig import ReadConf

host = ReadConf().get_mysql('host')
username = ReadConf().get_mysql('username')
password = ReadConf().get_mysql('password')
database = ReadConf().get_mysql('database')

DB_NAME = 'employees'
TABLES = {}

TABLES['employees'] = (
	"CREATE TABLE `employees` ("
	"  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
	"  `birth_date` date NOT NULL,"
	"  `first_name` varchar(14) NOT NULL,"
	"  `last_name` varchar(16) NOT NULL,"
	"  `gender` enum('M','F') NOT NULL,"
	"  `hire_date` date NOT NULL,"
	"  PRIMARY KEY (`emp_no`)"
	") ENGINE=InnoDB")

TABLES['departments'] = (
	"CREATE TABLE `departments` ("
	"  `dept_no` char(4) NOT NULL,"
	"  `dept_name` varchar(40) NOT NULL,"
	"  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
	") ENGINE=InnoDB")

TABLES['salaries'] = (
	"CREATE TABLE `salaries` ("
	"  `emp_no` int(11) NOT NULL,"
	"  `salary` int(11) NOT NULL,"
	"  `from_date` date NOT NULL,"
	"  `to_date` date NOT NULL,"
	"  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
	"  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
	"     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
	") ENGINE=InnoDB")

TABLES['dept_emp'] = (
	"CREATE TABLE `dept_emp` ("
	"  `emp_no` int(11) NOT NULL,"
	"  `dept_no` char(4) NOT NULL,"
	"  `from_date` date NOT NULL,"
	"  `to_date` date NOT NULL,"
	"  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
	"  KEY `dept_no` (`dept_no`),"
	"  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
	"     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
	"  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
	"     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
	") ENGINE=InnoDB")

TABLES['dept_manager'] = (
	"  CREATE TABLE `dept_manager` ("
	"  `dept_no` char(4) NOT NULL,"
	"  `emp_no` int(11) NOT NULL,"
	"  `from_date` date NOT NULL,"
	"  `to_date` date NOT NULL,"
	"  PRIMARY KEY (`emp_no`,`dept_no`),"
	"  KEY `emp_no` (`emp_no`),"
	"  KEY `dept_no` (`dept_no`),"
	"  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
	"     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
	"  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
	"     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
	") ENGINE=InnoDB")

TABLES['titles'] = (
	"CREATE TABLE `titles` ("
	"  `emp_no` int(11) NOT NULL,"
	"  `title` varchar(50) NOT NULL,"
	"  `from_date` date NOT NULL,"
	"  `to_date` date DEFAULT NULL,"
	"  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
	"  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
	"     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
	") ENGINE=InnoDB")


class MysqlDB(object):
	def __init__(self):
		self.conn = Connection(host, username, password, database)
		self.cursor = self.conn.cursor()

	def show_version(self):
		sql = 'select version()'
		self.cursor.execute(sql)
		# return a tuple
		data = self.cursor.fetchone()
		print('mysql version is {}'.format(data))

	def create_database(self):
		try:
			self.cursor.execute('create database %s charset utf8' % DB_NAME)
		except pymysql.err.MySQLError as e:
			print('failed creating database :{}'.format(str(e)))
			exit(1)

	def create_table(self):
		try:
			self.cursor.execute('USE {}'.format(DB_NAME))
		except pymysql.err.DatabaseError as err:
			print('use database {}'.format(str(err)))
			exit(1)

		try:
			for table_name in TABLES:
				table_des = TABLES[table_name]
				print('creating table: {}'.format(table_name))
				self.cursor.execute(table_des)
		except pymysql.err.MySQLError as e:
			print('crating table error {}'.format(str(e)))
			exit(1)
		else:
			print('OK')

	def insert(self):
		tomorrow = datetime.now().date() + timedelta(days=1)
		add_employee = '''insert into employees (first_name, last_name, hire_date, gender, birth_date) 
		values (%s, %s, %s, %s, %s)'''
		add_salary = '''insert into salaries values (%(emp_no)s, %(salary)s,%(from_date)s,%(to_date)s)'''
		data_employee = ('jack', 'ross', tomorrow, 'M', date(1977, 6, 16))
		# paramtrerize
		self.cursor.execute(add_employee, data_employee)
		emp_no = self.cursor.lastrowid
		print('the new emp_no is {}'.format(emp_no))

		data_salary = {
			'emp_no': emp_no,
			'salary': 50000,
			'from_date': tomorrow,
			'to_date': date(9999, 10, 1)
		}
		a = self.cursor.execute(add_salary, data_salary)
		self.conn.commit()
		print('execute return {}'.format(a))

	def delete(self):
		sql = '''delete from employees where emp_no > 100 '''
		effected = self.cursor.execute(sql)
		self.conn.commit()
		print("effected row {}". format(effected))

	def update(self):
		sql = '''update employees set first_name = "jack&rose" where emp_no=500011 '''
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except pymysql.MySQLError as e:
			print('failed update ')

	def retrieve(self):
		sql = '''select first_name, last_name, hire_date from employees where hire_date between %s and %s 
		order by hire_date asc'''
		hire_date = date(1999, 1, 1)
		end_date = date(1999, 1, 3)
		self.cursor.execute(sql, (hire_date, end_date))
		for (first_name, last_name, hire_date) in self.cursor:
			print('{}, {} was hired on {:%d-%b-%Y}'.format(last_name, first_name, hire_date))

	def __del__(self):
		self.cursor.close()
		self.conn.close()


if __name__ == '__main__':
	msq = MysqlDB()
	msq.show_version()
	# msq.insert()
	# msq.retrieve()
	# msq.delete()
	# msq.insert()
	# msq.update()
