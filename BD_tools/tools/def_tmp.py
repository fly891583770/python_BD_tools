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

import hashlib
import urllib
import urllib2
import httplib 

import sys
import json
import string

#默认为道客快分享,1:为道客快分享签名,2:帮忙拉签名
Send_Sms_TYPE = (
	('','默认--道客快分享签名'),
	('1','1--道客快分享签名'),
	('2','2--帮忙拉签名'),
)

# 点6
appKey = "2064302565"
secret = "BB9318B102E320C09B8AB9D5229B5668DB1C00D0"

global_env_flag = ""

def my_urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

def dict_to_str(dict):
	return urllib.urlencode(dict)

#去掉空字符串


#---- http keyvalue request 
def http_post_keyvalue(api_host  , api_port  , api_url , body_dict ):

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
def http_post_forms(api_host  , api_port  , api_url , body_dict , request_filename = None, request_binary = None ):


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



def http_post_api(req , url, body_dict ,api_host , api_port , request_type = "keyvalue", request_filename = None , request_binary = None ):

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
		return http_post_keyvalue( tmp_api_host, tmp_api_port, url ,  body_dict )
	elif request_type =="forms":
		print( "=========start===http_post_forms" )
		return http_post_forms( tmp_api_host, tmp_api_port, url ,  body_dict , request_filename, request_binary )		



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


def get_sign(body_dict, appkey_v , secret_v ):
	body_dict['appKey'] = appkey_v
	body_dict['secret'] = secret_v
	tuple = sortedDictValues(body_dict)
	tmp_str = tuple_append(tuple)
	print("really get sign:", tmp_str )
	sign = hashlib.sha1(tmp_str).hexdigest().upper()
	print( sign )
	del body_dict['secret']
	return sign



def templateApp_weibo(req, template_form,  uri , api_action , api_html = "apiform.html", api_host = None, api_port = None, before_sign = None, after_sign = None , request_type = "keyvalue"):
	
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

			result_msg = http_post_api(req , uri, body_dict,  api_host, api_port , request_type , file_name , file_binary )
			object_data = json.loads(result_msg)

		except :
			print result_msg
			pass

		return render_to_response(api_html, {'form':form, "api_action": api_action ,  "api_account": req.session['username'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form, "api_action": api_action , "api_account": req.session['username'] })
