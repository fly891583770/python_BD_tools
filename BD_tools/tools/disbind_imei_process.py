#!/usr/bin/python
#-*- coding: UTF-8 -*- 

from django.template import loader,Context
from django.http import HttpResponse
from tools.models import modtools
from django.forms import *
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from tools.login_ing import *
# import tools.login_ing

# from tools.oauth_api import *
# from tools.client_custom_api import *
# from tools.reward_api import *

import hashlib
import urllib
import urllib2
import httplib 

import sys
import json
import string


# 解绑流程
def templateApp_Disbanding(req, template_form,  uri , api_action , api_name, api_html = "apimodel.html", api_host = None, api_port = None, before_sign = None, after_sign = None ):

	if req.method == 'POST':
		form = template_form(req.POST)
		req.session['environment'] = environment
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
		try:
			result_msg = http_post_api(req , uri,request_msg, api_host, api_port )
			object_data = json.loads(result_msg)
		except :
			print result_msg
			pass
		if not object_data :
			result_msg = "http error!"
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "result_msg":result_msg })
		
		if object_data["ERRORCODE"] and object_data["ERRORCODE"] != "0" :
			return render_to_response(api_html, {'form':form,  "api_name":api_name, "api_action": api_action , "result_msg":result_msg })

		if not object_data["RESULT"]["accountID"] and object_data["ERRORCODE"] == "0" :
			result_msg = "该用户没有绑定imei!"
			return render_to_response(api_html, {'form':form,  "api_name":api_name, "api_action": api_action, "result_msg":result_msg })
		else: 
 			accountID = object_data["RESULT"]["accountID"]

		# 解绑用户计算sign值
		dict = {} 
		server_url = "accountapi/v2/disconnectAccount"
		dict["accountID"] = accountID.encode('utf-8')

		dict['sign'] = get_sign(dict, tmp_appkey , tmp_secret)

		if after_sign != None:
			after_sign(dict)

		request_msg = ""
		request_msg = dict_to_str(dict)

		result_msg = ""
		object_data = None

		try:
			result_msg = http_post_api(req , server_url,request_msg, api_host, api_port )
			object_data = json.loads(result_msg)
		except :
			print result_msg
			pass
		return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form, "api_name":api_name, "api_action": api_action ,  "api_name":api_name, "api_account": req.session['accountID'] })

#=====================================================================
#得到终端信息
class classGetMirrtalkInfoByImei(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label= "IMEI" )

def getMirrtalkInfoByImei(req):
	api_uri = "accountapi/v2/getMirrtalkInfoByImei"
	return templateApp_Disbanding(req, classGetMirrtalkInfoByImei, api_uri , sys._getframe().f_code.co_name, "WEME终端机解绑")

#注销用户
class classCancellationAccount(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label= "手机号")
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label= "账户编号")

def cancellationAccount(req):
	api_uri = "accountapi/v2/cancellationAccount"
	return templateAppCancle(req, classCancellationAccount, api_uri , sys._getframe().f_code.co_name, "注销用户或解绑手机号")