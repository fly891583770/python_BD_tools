#!/usr/bin/python
#-*- coding: UTF-8 -*- 

from django.template import loader,Context
from django.http import HttpResponse
from tools.models import modtools
from django.forms import *
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from environment_models import *

import MySQLdb
import hashlib
import urllib
import urllib2
import httplib 
import logging
import smtplib
import time

import sys
import json
import string
import socket

# appkey
global_env_flag = ""

# 获取本地ip
# def get_ip_address():
# 	host_name = socket.gethostname()
# 	ip_address = socket.gethostbyname(host_name)
# 	return ip_address

def my_urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

def http_post_api(req , url, data ,api_host , api_port ):
	tmp_api_host = ""
	tmp_api_port = 0

	if api_host != None and api_port != None :
		tmp_api_host = api_host
		tmp_api_port = api_port
	else:

		tmp_env_flag = req.session['environment']

		tmp_api_host = api_server_list[tmp_env_flag]
		tmp_api_port = api_post_list[tmp_env_flag]

	requrl = "http://{0}:{1}/{2}".format( tmp_api_host , tmp_api_port , url )

	print(requrl)

	try:
		headerdata = {"Host": tmp_api_host }
		conn = httplib.HTTPConnection(tmp_api_host,tmp_api_port)
		conn.request(method="POST",url = requrl, body = data, headers = headerdata) 

		# conn.request(method="POST",url = requrl, body = data ) 

		response = conn.getresponse()
		res= response.read()
		return res
	except:
	 	return  "http request failed : " +  requrl 

def http_get_api(req , url, requrl ,api_host , api_port ):
	tmp_api_host = ""
	tmp_api_port = 0

	if api_host != None and api_port != None :
		tmp_api_host = api_host
		tmp_api_port = api_port
	else:
		tmp_env_flag = req.session['environment']
		tmp_api_host = api_server_list[tmp_env_flag]
		tmp_api_port = api_post_list[tmp_env_flag]

	try:
		conn = httplib.HTTPConnection(tmp_api_host,tmp_api_port)
		conn.request('GET', '/'+url+requrl) 
		print '/'+url+requrl
		response = conn.getresponse()
		res= response.read()
		print tmp_api_host
		print tmp_api_port
		return res
	except:
	 	return  "http request failed : " +  requrl 
	finally:
		conn.close()

def dict_to_str(dict):
	return urllib.urlencode(dict)

def tuple_to_str(tuple):
	string = ""
	for k, v in enumerate(tuple):
		if len(string) == 0 :
			string = str(v[0]) + "=" + my_urlencode(str(v[1]))
		else:
			string = string + "&" + str(v[0]) + "=" + my_urlencode(str(v[1]))
	return string

def tuple_append(tuple):
	string = ""
	for k, v in enumerate(tuple):
		if len(string) == 0 :
			string = str(v[0]) + str(v[1])
		else:
			string = string + str(v[0]) + str(v[1])
	return string


def sortedDictValues(adict): 
	items = adict.items() 
	items.sort() 
	return [ (key, value) for key, value in items] 


def get_sign(dict, appkey_v , secret_v ):
	dict['appKey'] = appkey_v
	dict['secret'] = secret_v
	tuple = sortedDictValues(dict)
	tmp_str = tuple_append(tuple)
	print("really get sign:", tmp_str )
	sign = hashlib.sha1(tmp_str).hexdigest().upper()
	print( sign )
	del dict['secret']
	return sign


def templateAppCancle(req, template_form,  uri , api_action , api_name, api_html = "apiform.html" , api_host = None, api_port = None, before_sign = None, after_sign = None ):
	if req.method == 'POST':
		form = template_form(req.POST)
		dict = {}
		for item in req.POST:
			dict[item] = req.POST[item].encode('utf-8')

		if  req.session['accountID'] != 'kxl1QuHKCD' :
			result_msg = '{"警告":"管理员权限不够"}'
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action, "api_account": req.session['accountID'],"uri": uri, "result_msg":result_msg} )
			pass

		if req.POST['accountID'].encode('utf-8') == 'kxl1QuHKCD' or req.POST['mobile'].encode('utf-8') == '15921420950' :
			result_msg = '{"错误提示":"当前为频道管理员账号，不能对其操作"}'
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action, "api_account": req.session['accountID'],"uri": uri, "result_msg":result_msg} )

		if before_sign != None:
			before_sign(dict)

		tmp_appkey = appKey
		tmp_secret = secret
		
		if req.session['appKey'] and req.session['secret']:
			tmp_appkey = req.session['appKey']
			tmp_secret = req.session['secret']

		dict['sign'] = get_sign(dict, tmp_appkey , tmp_secret)

		if after_sign != None:
			after_sign(dict)

		request_msg = dict_to_str(dict)

		result_msg = ""
		object_data = None

		try:
			result_msg = http_post_api(req , uri,request_msg, api_host, api_port )
			object_data = json.loads(result_msg)
		except :
			print result_msg
			pass

		return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] })



def templateApp_Batch(req, template_form,  uri , api_action , api_name, api_html = "apimodel.html" , api_host = None, api_port = None, before_sign = None, after_sign = None ):
	if req.method == 'POST':
		form = template_form(req.POST)
		dict = {} 
		for item in req.POST:
			dict[item] = req.POST[item].encode('utf-8')

		if before_sign != None:
			before_sign(dict)

		tmp_appkey = appKey
		tmp_secret = secret
		
		if req.session['appKey'] and req.session['secret']:
			tmp_appkey = req.session['appKey']
			tmp_secret = req.session['secret']

		dict['sign'] = get_sign(dict, tmp_appkey , tmp_secret)

		if after_sign != None:
			after_sign(dict)

		request_msg = dict_to_str(dict)

		result_msg = ""
		object_data = None 
		totalList=req.POST['totalList']

		if int(totalList.count(","))+1 > 1000:
			result_msg = '{"错误提示":"拉粉人数超过1000个"}'
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )

		try:
			result_msg = http_post_api(req , uri,request_msg, api_host, api_port )
			object_data = json.loads(result_msg)
		except :
			print result_msg
			pass

		
		return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] })


def mysqladdrs(sqladdr):
	mysqladd = {
		'user_center' : {
			'host' : "192.168.1.17",
			'user' : "observer",
			'passwd' : "abc123",
			'db' : "crowdRewards",
		}
	}
	user_dict = mysqladd[sqladdr]
	return user_dict

def mysql_pool(sql):
	if sql :
		dict_tab = mysqladdrs("user_center")
		host = dict_tab['host']
		user = dict_tab['user']
		passwd = dict_tab['passwd']
		db = dict_tab['db']

		# 打开数据库连接
		conn=MySQLdb.connect(host= host, user= user, passwd=passwd, db= db, charset="utf8")
		# 使用cursor()方法获取操作游标
		cursor = conn.cursor()
		try:
			str1 = cursor.execute(sql)
			#提交到数据库执行,执行commit()命令
			# db.commit()
		except Exception as err:

			#失败回滚数据
			conn.rollback()
		#获取所有查询结果
		results = cursor.fetchall()

		# 关闭数据库
		conn.close()
		return results

def python_log(req, environment, uri):
	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='mypython.log', filemode='a')

	curl_url = "environment: {0} username: {1} http://{2}:{3}/{4} POST ".format(environment, req.session['username'], api_server_list[environment], api_post_list[environment], uri)
	logging.warning( curl_url ) 

def python_log_msg(req, environment, uri, request_msg):

	logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='mypython.log', filemode='a')

	curl_url = "environment: {0} username: {1} http://{2}:{3}/{4} POST {5}".format(environment, req.session['username'], api_server_list[environment], api_post_list[environment], uri, request_msg)
	logging.warning( curl_url ) 

def tuple_to_str(accountIDs):

	str_tx = accountIDs.split(',')
	results = ""
	for value in str_tx:
		results = results+ "'" + value + "',"

	results = results[:-1]
	print("results222===",results)
	return results

def user_info(req, template_form, uri, api_action, api_name, request_type = "keyvalue"):

	if uri == "getBusinessInfo": 
		table_date = ('企业名称','企业编号','应用标识','账号','创建时间','父渠道ID','用户名','电话','地址','备注')		
	elif uri == "getUserMoneyType": 
		table_date = ('用户账号','资金类型','备注')
	python_log(req, environment, uri)

	if req.method == 'POST':

		form = template_form(req.POST)

		if uri == "getBusinessInfo": 

			businessName= req.POST['businessName'].encode('utf-8')

			if "'" in businessName:
				form = template_form()
				return render_to_response('sqlmodel.html',{'form':form,"api_name":api_name, "api_action": api_action , "api_account": req.session['username'],"table_date":table_date })
				 
			execute_sql = "SELECT name,businessID,appKey,accountID,from_unixtime(createTime),parentID,receiverName,receiverPhone,receiverAddress,remark FROM businessInfo where name like " + "'%" +businessName+ "%'" +"order by id desc limit 30"
			print(execute_sql)
			request_msg = mysql_pool(execute_sql)

		elif uri == "getUserMoneyType": 

			accountIDs= req.POST['accountID'].encode('utf-8')

			if "'" in accountIDs:
				form = template_form()
				return render_to_response('sqlmodel.html',{'form':form,"api_name":api_name, "api_action": api_action , "api_account": req.session['username'],"table_date":table_date })

			results = tuple_to_str(accountIDs)
			execute_sql = "SELECT accountID,moneyType ,case when moneyType=1 then '密点'  when moneyType=3 then '保险预购金' when moneyType=4 then '返企业奖金' end as 'remarks' FROM crowdRewards.userMoneyInfo WHERE accountID in( " + results + " ) order by moneyType limit 10 "
			print(execute_sql)
			request_msg = mysql_pool(execute_sql)

		return render_to_response('sqlmodel.html', {'form':form, "api_name":api_name,"api_action": api_action ,"request_msg":request_msg,"table_date":table_date} )
	else:
		form = template_form()
		return render_to_response('sqlmodel.html',{'form':form,"api_name":api_name, "api_action": api_action , "api_account": req.session['username'],"table_date":table_date })


def templateApp(req, template_form,  uri , api_action , api_name, api_html = "apimodel.html" , api_host = None, api_port = None, before_sign = None, after_sign = None, request_type = "keyvalue" ):

	if req.method == 'POST':
		form = template_form(req.POST)
		dict = {} 
		for item in req.POST:
			dict[item] = req.POST[item].encode('utf-8')

		if before_sign != None:
			before_sign(dict)

		tmp_appkey = appKey
		tmp_secret = secret
		
		if req.session['appKey'] and req.session['secret']:
			tmp_appkey = req.session['appKey']
			tmp_secret = req.session['secret']

		if uri == 'accountapi/v2/quickCreateImei' :
			dict['useType'] = "1"
		dict['sign'] = get_sign(dict, tmp_appkey , tmp_secret)

		if after_sign != None:
			after_sign(dict)

		request_msg = dict_to_str(dict)
		result_msg = ""
		object_data = None

		python_log_msg(req, environment, uri, request_msg)

		if uri == 'accountapi/v2/setCustomArgs' and req.POST['accountID'].encode('utf-8') == '' :
			model = req.POST['model'].encode('utf-8')
			if (model == 'SG900' or model == 'TG900') :
				result_msg = '{"ERRORCODE": "ME01023","错误提示": "这个model = ' + model +'不支持！！！！！"}'
				return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )

		if uri == 'accountapi/v2/quickCreateImei'  and req.POST['mirrtalkCount'].encode('utf-8') !='' and int(req.POST['mirrtalkCount']) > 1000  :
			result_msg = '{"ERRORCODE": "ME01023","错误提示":"创建imei数超过1000个"}'
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
		
		try:
			result_msg = http_post_api(req , uri, request_msg,  api_host, api_port  )
			object_data = json.loads(result_msg)
			

		except Exception as error:
			print " error %s" % error
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
			pass

		if object_data["ERRORCODE"] == 'ME18312' and uri == 'clientcustom/v2/transferSecretChannel' :
			result_msg = '{"ERRORCODE": "ME18312","错误提示": "接受者未加入当前频道，转移失败"}'
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
		
		if uri == 'accountapi/v2/quickCreateImei' and  object_data['ERRORCODE'] == "0":
			table_date = ('设备串号','押金密码')
			useType = 1				
			return render_to_response('sqlmodel.html', {'form':form, "api_name":api_name,"api_action": api_action , "useType":useType,"request_msg":request_msg,  "object_data":object_data['RESULT'], "table_date":table_date} )

		#if uri == 'rewardapi/v2/queryDeviceStatus' and  object_data['ERRORCODE'] == "0":
		#	table_date = ('imei(终端串号)','是否激活','是否绑定账户','绑定账户','里程奖金返还对象(1:个人,4:企业)','酬谢最大金额','八月里程奖金','九月里程奖金','十月里程奖金','十一月里程奖金','八月押金','九月押金','十月押金','十一月押金','账户余额','企业里程奖金返还总月数','押金类型','冻结的押金金额','是否为买断机','是否为押金机','是否为备用机','开机时间','是否换货','换货前imei','换货后imei','备注')
		#	useType = 2		
		#	return render_to_response('sqlmodel.html', {'form':form, "api_name":api_name,"api_action": api_action , "useType":useType,"request_msg":request_msg,  "object_data":object_data['RESULT'], "table_date":table_date} )
		return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )

	else:
		form = template_form()
		python_log(req, environment, uri)
		return render_to_response(api_html,{'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] })

def templateApp_Get(req, template_form,  uri , api_action , api_name, api_html = "apimodel.html" , api_host = None, api_port = None, before_sign = None, after_sign = None, request_type = "keyvalue" ):

	if req.method == 'POST':
		form = template_form(req.POST)

		result_msg = ''
		request_msg = ''
		object_data = None

		python_log_msg(req, environment, uri, request_msg)

		if uri == 'crazyapi/v2/autorepairnicknameurl':
			imei = req.POST['imei'].encode('utf-8')
			jobId = 'DBChoose_'+time.strftime('%Y-%m-%d',time.localtime(time.time()))
			request_msg = '?imei='+imei+'&jobId='+jobId

		if request_msg == '':
			result_msg = "参数错误！"+object_data["ERRORCODE"].encode('utf-8') +object_data["RESULT"].encode('utf-8')
			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg } )

		print '\nxxxx%s\n' % request_msg
		try:
			result_msg = http_get_api(req , uri, request_msg,  api_host, api_port  )
			object_data = json.loads(result_msg)

		except Exception as error:
			print " error %s" % error
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
			pass

		return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )

	else:
		form = template_form()
		python_log(req, environment, uri)
		return render_to_response(api_html,{'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] })



def templateApp_Debug(req, template_form,  uri , api_action , api_name, api_html = "user_login.html", api_host = None, api_port = None, before_sign = None, after_sign = None ):
	if req.method == 'POST':
		form = template_form(req.POST)
		for item in req.POST:
			dict[item] = req.POST[item].encode('utf-8')
			if item == "appKey":
				req.session['appKey'] = req['appKey']
			elif item == "secret":
				req.session['secret'] = req['secret']

		print(req.session['appKey'])
		print(req.session['secret'])

		return render_to_response(api_html, {'form':form,  "api_name":api_name, "api_action": api_action ,  "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form,  "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] })


#登陆
def templateApp_Login(req, template_form,  uri , api_action , api_html = "user_login.html", api_host = None, api_port = None, before_sign = None, after_sign = None ):

	if req.method == 'POST':
		form = template_form(req.POST)
		req.session['environment'] = environment
		# clientIP = get_ip_address()
		dict = {} 
		# dict["clientIP"] = clientIP
		for item in req.POST:
			dict[item] = req.POST[item].encode('utf-8')

		act_dict = {}
		act_dict['xiaoTian']= '15921420950'
		act_dict['jiangZs']	= '18221526560'
		act_dict['zhaoWl']	= '18117359981'
		act_dict['yuLi']	= '18616672387'
		act_dict['zhouZ']	= '18217656820'
		act_dict['xueTy']	= '13052190959'
		act_dict['liuMl']   = '15000296472'
		act_dict['liC'] = '15214389427'
		flage=0
		for account in act_dict:
			if act_dict[account] == req.POST["username"]:
				flage = 1
				req.session['username'] = req.POST["username"]
				break
			pass

		if flage != 1:
			result_msg = "账号"+req.POST["username"].encode('utf-8')+"权限不够"
			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg } )
			pass

		if before_sign != None:
			before_sign(dict)

		tmp_appkey = appKey
		tmp_secret = secret

		dict['sign'] = get_sign(dict, tmp_appkey , tmp_secret)

		if after_sign != None:
			after_sign(dict)

		request_msg = dict_to_str(dict)
		server_url = "accountapi/v2/checkLogin"
		result_msg = ""
		object_data = None

		try:
			result_msg = http_post_api(req, server_url, request_msg, api_host, api_port )
			object_data = json.loads(result_msg)
		except :
			print result_msg
			pass

		if not object_data :
			result_msg = "http error!"
			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg } )

		if object_data["ERRORCODE"] != '0' :
			result_msg = "账户信息错误！"+object_data["ERRORCODE"].encode('utf-8') +object_data["RESULT"].encode('utf-8')
			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg } )
		else:
			accountID = object_data["RESULT"]["accountID"]

		logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w+')

		if accountID and len(accountID) == 10:
			req.session['accountID'] = accountID
			if tmp_appkey != None and tmp_secret != None :
				req.session['appKey'] = tmp_appkey
				req.session['secret'] = tmp_secret
			return HttpResponseRedirect("index")
		else:
			result_msg = "accountID不正确"
			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form, "api_action": api_action  })


#=======================================login begin=========================================================================

class classUserLogin(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "用户名")
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "密码")

def login(req):
	api_uri = ""
	return templateApp_Login(req, classUserLogin, api_uri , sys._getframe().f_code.co_name, api_html = "user_login.html" )

def logout(req):
	accountID = req.session.get('accountID')
	if accountID:
		del req.session['accountID']

	if req.session['environment']:
		del req.session['environment']

	if req.session['appKey']:
		del req.session['appKey']

	if req.session['secret']:
		del req.session['secret']

	if req.session['username']:
		del req.session['username']

	return HttpResponseRedirect("login") 

def left(req):
	accountID = req.session.get('accountID')
	if accountID:
		return render_to_response('left.html', { 'accountID' : req.session['accountID'] } )
	else:
		return HttpResponseRedirect("login") 

def right(req):
	accountID = req.session.get('accountID')
	if accountID:
		return render_to_response('right.html', { 'accountID' : req.session['accountID'] } )
	else:
		return HttpResponseRedirect("login") 

def top(req):
	accountID = req.session.get('accountID')
	if accountID:

		tmp_env_flag = req.session['environment']
		server = api_remark_list[tmp_env_flag]
		host = api_server_list[tmp_env_flag] 
		port = api_post_list[tmp_env_flag]
		username = req.session['username']
		tmp_appkey = appKey 
		if req.session['appKey']:
			tmp_appkey = req.session['appKey']

		tmp_secret = secret 
		if req.session['secret']:
			tmp_secret = req.session['secret']

		return render_to_response('top.html', { 'username' : username ,'accountID' : accountID , 'server' : server , "host" : host , "port" : port , "appkey":tmp_appkey ,"secret":tmp_secret } )
	else:
		return HttpResponseRedirect("login") 

def index(req):
	accountID = req.session.get('accountID')
	if accountID:
		return render_to_response('index.html', { 'accountID' : accountID  } )
	else:
		return HttpResponseRedirect("login") 
#-------------------------------login end--------------------------------------------------------------------


#---- http keyvalue request 
def http_post_keyvalue_save_file(api_host  , api_port  , api_url , body_dict ):

	requrl = "http://{0}:{1}/{2}".format( api_host , api_port , api_url )

	print(requrl)

	headerdata = {"Host": api_host }
	data_value =  dict_to_str(body_dict)

	try:
		conn = httplib.HTTPConnection(api_host,api_port)
		conn.request(method="POST",url = requrl, body = data_value, headers = headerdata) 
		response = conn.getresponse()
		res= response.read()
		return res
	except:
	 	return  "http request failed : " +  requrl 

#---- http forms request 
def http_post_forms_save_file(api_host  , api_port  , api_url , body_dict , request_filename = None, request_binary = None ):


	http_url = "http://{0}:{1}/{2}".format( api_host , api_port , api_url )

	print(http_url)

	bounary = "---------------------------current-is-python-api-debug-tools"

	http_body = ""

	for item in body_dict:
		if http_body != "":
			http_body = http_body + "\r\n--{0}".format(bounary)
		else:
			http_body = http_body + "--{0}".format(bounary)
		
		http_body = http_body + '\r\nContent-Disposition: form-data; name="{0}"\r\n'.format(item)
		http_body = http_body + '\r\n{0}'.format(body_dict[item])


	print("=======START=====")

	# body_data = []

	# if request_filename != None and request_binary != None:

	# 	print "-----------forms--------2----------"

	# 	body_data.append("--%s" % bounary)

	# 	print "-----------forms--------3----------"

	# 	body_data.append('Content-Disposition: form-data; name="mmfile"; filename="%s"\r\n' %  ( request_filename ) )

	# 	print "-----------forms--------4----------"

	# 	body_data.append("Content-Type: application/octet-stream\r\n\r\n")

	# 	print "-----------forms--------5----------"

	# 	body_data.append(request_binary)

	# 	print "-----------forms--------6----------"

	# 	body_data.append("\r\n")

	# 	print "-----------forms--------7----------"


	# print "-----------forms--------8----------"

	# body_data.append("--%s--" % bounary)


	try:

		print("type(http_body): ", type(http_body)) 

		if request_filename != None and request_binary != None:

			print("type(request_binary): str ", type(request_binary)) 

			print "-----------forms--------2----------"

			http_body  = http_body + "\r\n--{0}".format(bounary)

			print "-----------forms--------3----------"

			http_body  = http_body + '\r\nContent-Disposition: form-data; name="mmfile"; filename="{0}"'.format(request_filename)

			print "-----------forms--------4----------"

			http_body  = http_body + "\r\nContent-Type: application/octet-stream\r\n"

			print "-----------forms--------5----------"

			http_body  = http_body + "\r\n"

			print "-----------forms--------6----------"

			print "-----------forms--------7----------"

			http_body  = http_body + request_binary

			print "-----------forms--------8----------"

	except Exception as err:
		print "error============="
		print err


	http_body = http_body + "\r\n--{0}--".format(bounary)


	result_msg = ""

	try:
		req = urllib2.Request( http_url, data = http_body )
		req.add_header("Content-Type", "multipart/form-data; boundary=%s" % bounary  )
		req.add_header("User-Agent","python api-debug-tools")
		res = urllib2.urlopen(req, timeout = 50 )
		result_msg = res.read()
	except Exception as err:
		result_msg = err.fp.read()
	finally:
		return result_msg



def http_post_api_save_file(req , url, body_dict ,api_host , api_port , request_type = "keyvalue", request_filename = None , request_binary = None ):

	tmp_api_host = ""
	tmp_api_port = 0

	if api_host != None and api_port != None :
		tmp_api_host = api_host
		tmp_api_port = api_port
	else:

		tmp_env_flag = req.session['environment']

		tmp_api_host = api_server_list[tmp_env_flag]
		tmp_api_port = api_post_list[tmp_env_flag]

	if request_type== None or request_type == "keyvalue":
		print( "=========start===http_post_keyvalue" )
		return http_post_keyvalue_save_file( tmp_api_host, tmp_api_port, url ,  body_dict )
	elif request_type =="forms":
		print( "=========start===http_post_forms" )
		return http_post_forms_save_file( tmp_api_host, tmp_api_port, url ,  body_dict , request_filename, request_binary )		

def template_save_file(req, template_form,  uri , api_action, api_name, api_html = "apiform.html", api_host = None, api_port = None, before_sign = None, after_sign = None , request_type = "keyvalue"):
	
	if req.method == 'POST':

		print "========current post templateApp======="

		form = template_form(req.POST)
		body_dict= {} 
		
		for item in req.POST:
			body_dict[item] = req.POST[item].encode('utf-8')

		if uri == 'accountapi/v2/quickCreateImei' :
			body_dict['useType'] = "1"



		# print "====debug==info=========="
		# print "req.FILES " ,req.FILES

			
		file_name = ""
		file_count = 0 
		file_binary = None

		for tmp_file in req.FILES:
			file_count = file_count + 1
			file_key = tmp_file


		if file_count == 1:

			# 一次只能上传一个文件

			# print "req.FILES[" + file_key + "] ",req.FILES.get(file_key,None)
			
			file_name = req.FILES.get(file_key,None)


			file_binary = req.FILES.get(file_key,None).read()
			
			

			# print "body_dict add length " , len(file_binary)

			#  是业务决定的 
			body_dict["length"] = len(file_binary)


		else:

			print "====debug==error====upload file count======", file_count


		if before_sign != None:
			before_sign(body_dict)

		tmp_appkey = appKey
		tmp_secret = secret

		if req.session['appKey'] and req.session['secret']:
			tmp_appkey = req.session['appKey']
			tmp_secret = req.session['secret']

		body_dict['sign'] = get_sign(body_dict, tmp_appkey , tmp_secret)

		if after_sign != None:
			after_sign(body_dict)

		request_msg = dict_to_str(body_dict)

		result_msg = ""
		object_data = None
		
		try:

			result_msg = http_post_api_save_file(req , uri, body_dict,  api_host, api_port , request_type , file_name , file_binary )
			object_data = json.loads(result_msg)

		except :
			print result_msg
			pass

		return render_to_response(api_html, {'form':form, "api_action": api_action ,  "api_account": req.session['username'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form, "api_action": api_action , "api_account": req.session['username'] })
