#!/bin/bash/evn python
# encoding=utf-8
"""
@file:send_email.py
@time:5/25/20|2:16 PM
"""
import os
import time
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from readConfig import ReadConf
from getPathInfo import get_path
path = get_path()

report_path = os.path.join(path, 'result', 'report.html')

def send_email():
	rd = ReadConf()
	sender = rd.get_email('sender')
	address = rd.get_email('address')
	port = rd.get_email('port')
	cc = rd.get_email('cc')
	subject = rd.get_email('subject') + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	with open(report_path, 'r') as f:
		mail_body = f.read()
	str_msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')

	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = address
	msg.attach(str_msg)
	smt = SMTP()
	try:
		smt.connect('smtp.163.com', port)
		smt.login(user='', password='')
	except:
		print('login email failed')
	else:
		smt.send_message(msg, sender, [address, cc])
	finally:
		smt.quit()


if __name__ == '__main__':
	print(report_path)
