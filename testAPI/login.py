#!/bin/bash/evn python
# encoding=utf-8
"""
@file:login.py
@time:5/24/20|10:39 PM
"""
import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/login', methods=['POST', "GET"])
def login():
	username = 'jack'
	pwd = 'jack11'

	v_u = request.values.get('username')
	v_p = request.values.get('password')

	if v_u == username and v_p == pwd:
		resp = {'errmsg': 'login success', 'errcode': 200}
	else:
		if not all([v_u, v_p]):
			resp = {'errmsg': "not enough params", 'errcode': -1}
		else:
			resp = {'errmsg': "username or password not correct", 'errcode': 1000}

	return json.dumps(resp)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)