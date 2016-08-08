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




#===============REWARD BEGIN==================

REWARD_RETURN_TYPE =  (
	('1','1--个人'),
	('2','2--企业'),
	('3','3--混合'),
)

REWARD_PARENT_ID = (
	('0','0--否'),
	('1','1--是'),
)

REWARD_IS_CHANNEL = (
	('0','0--否'),
	('1','1--是'),
)

REWARD_ALLOW_EXCHANGE = (
	('0','0--不允许'),
	('1','1--允许'),	
)

REWARD_BONUS_TYPE = (
	('0','0--无奖金'),
	('1','1--密点'),	
	('2','2--微点'),
	('4','4--其它方式'),
)

REWARD_SHARE_INFO = (
	('0','0--不分享'),
	('1','1--分享'),
)

REWARD_BONUS_RETURN_TARGET_TYPE = (
	('1','1--个人'),
	('2','2--个人与企业,个人优先'),	
	('3','3--个人与企业,企业优先'),
	('4','4--企业'),
)

#isAnonymous
#0代表不匿名,1代表匿名
REWARD_IS_ANONYMOUS =  (
	('0','0--不匿名'),
	('1','1--匿名'),
)

#是否有效
VALIDITY_TYPE = (
	('0','0--无效'),
	('1','1--有效'),

)

# imei默认状态码
IMEI_STATUS = (
	('','10a--工厂生产'),
	('13g','13g--语境发货'),

)

#是否是第三方model
IS_THIRD_MODEL = (
	('0','0----普通渠道商'),
	('1','1----第三方车机用户'),
)

#使用类型。1:企业用户,2:开发者用户,3:其他',
USE_TYPE = (
	('1','1----企业用户'),
	('2','2----开发者用户'),
	('3','3----其他'),
)

#是否是第三方model
MIRRTALK_HISTORY_REMARKS = (
	('工厂申请语镜imei号码','0----工厂申请语镜imei号码'),
)


DOMAIN_ADDRE = (
	('s9d1.mirrtalk.com','生产环境域名地址(s9d1.mirrtalk.com)'),
)
#===============REWARD END====================


# def templateApp_creat_imei (req, template_form,  uri , api_action , api_html = "apiform.html", api_host = None, api_port = None, before_sign = None, after_sign = None ):
# def templateApp_creat_imei (req, template_form,  uri , api_action , api_name, api_html = "apimodel.html", api_host = None, api_port = None, before_sign = None, after_sign = None ):

# 	if req.method == 'POST':
# 		form = template_form(req.POST)
# 		req.session['environment'] = environment

# 		dict = {} 
# 		dict["username"] = req.POST["username"].encode('utf-8')
# 		dict["mobile"] = req.POST["mobile"].encode('utf-8')
# 		dict["businessName"] = req.POST["businessName"].encode('utf-8')
# 		dict["returnType"] = req.POST["returnType"].encode('utf-8')
# 		dict["parentID"] = req.POST["parentID"].encode('utf-8')
# 		dict["isChannel"] = req.POST["isChannel"].encode('utf-8')
# 		dict["receiverName"] = req.POST["receiverName"].encode('utf-8')
# 		dict["receiverPhone"] = req.POST["receiverPhone"].encode('utf-8')
# 		dict["receiverAddress"] = req.POST["receiverAddress"].encode('utf-8')
# 		dict["allowExchange"] = req.POST["allowExchange"].encode('utf-8')
# 		dict["bonusType"] = req.POST["bonusType"].encode('utf-8')
# 		dict["shareInfo"] = req.POST["shareInfo"].encode('utf-8')
# 		dict["bonusReturnTarget"] = req.POST["bonusReturnTarget"].encode('utf-8')
# 		dict["userBonusMax"] = req.POST["userBonusMax"].encode('utf-8')
# 		dict["businessBonusMax"] = req.POST["businessBonusMax"].encode('utf-8')
# 		dict["bonusReturnMonth"] = req.POST["bonusReturnMonth"].encode('utf-8')
# 		dict["remark"] = req.POST["remark"].encode('utf-8')


# 		if before_sign != None:
# 			before_sign(dict)

# 		tmp_appkey = appKey
# 		tmp_secret = secret
# 		if req.session['appKey'] and req.session['secret'] :
# 			tmp_appkey = req.session['appKey']
# 			tmp_secret = req.session['secret']

# 		dict['sign'] = get_sign(dict, tmp_appkey, tmp_secret)

# 		if after_sign != None :
# 			after_sign(dict)

# 		request_msg = dict_to_str(dict)

# 		result_msg = ""
# 		object_data = None
# 		try :
# 			result_msg = http_post_api(req , uri,request_msg, api_host, api_port )
# 			object_data = json.loads(result_msg)
# 		except :
# 			print result_msg
# 			pass

# 		if not object_data :
# 			result_msg = "http error!"
# 			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg })

# 		if object_data["ERRORCODE"] and object_data["ERRORCODE"] != "0" :
# 			result_msg = object_data["RESULT"]
# 			return render_to_response(api_html, {'form':form, "api_action": api_action , "result_msg":result_msg })
# 		else :
#  			new_appKey = object_data["RESULT"][0]["appKey"]
#  			new_businessID = object_data["RESULT"][0]["id"]

#  		dict_imei = {}
# 		dict_imei["company"] = req.POST["businessName"].encode('utf-8')
# 		dict_imei["model"] = req.POST["model"].encode('utf-8')
# 		dict_imei["isThirdModel"] = req.POST["isThirdModel"].encode('utf-8')
# 		dict_imei["mirrtalkCount"] = req.POST["mirrtalkCount"].encode('utf-8')
# 		dict_imei["mirrtalkInforemarks"] = req.POST["mirrtalkInforemarks"].encode('utf-8')
# 		dict_imei["mirrtalkHistoryremarks"] = req.POST["mirrtalkHistoryremarks"].encode('utf-8')
# 		dict_imei["clientIP"] = req.POST["clientIP"].encode('utf-8')
		
# 		dict_imei["clientappKey"] = new_appKey.encode('utf-8')
# 		dict_imei["businessID"] = new_businessID.encode('utf-8')

# 		dict_imei['sign'] = get_sign(dict_imei, tmp_appkey , tmp_secret)

# 		server_url = "accountapi/v2/createImei"
		
# 		if after_sign != None :
# 			after_sign(dict_imei)

# 		request_msg = ""
# 		request_msg = dict_to_str(dict_imei)

# 		result_msg = ""
# 		object_data = None

# 		try:
# 			result_msg = http_post_api(req , server_url,request_msg, api_host, api_port )
# 			object_data = json.loads(result_msg)
# 		except:
# 			print result_msg
# 			pass
		
# 		return render_to_response(api_html, {'form':form, "api_action": api_action ,  "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
# 	else:
# 		form = template_form()
# 		return render_to_response(api_html,{'form':form, "api_action": api_action , "api_account": req.session['accountID'] })

# def transfer_api(dict, uri, appKey_api):

# 	tmp_appkey = appKey
# 	tmp_secret = secret
# 	if appKey_api and len(appKey_api) != 0 :
# 		tmp_appkey = appKey_api

# 	# sign 计算
# 	dict['sign'] = get_sign(dict, tmp_appkey , tmp_secret)

# 	# dict to kv
# 	request_msg = dict_to_str(dict)

# 	result_msg = ""
# 	object_data = None
	
# 	try:
# 		result_msg = http_post_api(req , uri,request_msg, api_host, api_port )
# 		object_data = json.loads(result_msg)
# 	except :
# 		print result_msg
# 		pass
# 	pass

# 	return request_msg, result_msg, object_data

def templateApp_creatImei_setArgs( req, template_form,  uri, api_action, api_name, api_html = "apimodel.html", api_host = None, api_port = None, before_sign = None, after_sign = None ):
	
	if req.method == 'POST':
		form = template_form(req.POST)
		req.session['environment'] = environment

		# # 生成IMEI参数
		dict_imei = {}
		dict_imei["clientappKey"] = req.POST["clientappKey"].encode('utf-8')
		dict_imei["company"] = req.POST["company"].encode('utf-8')
		dict_imei["model"] = req.POST["model"].encode('utf-8')
		dict_imei["status"] = req.POST["status"].encode('utf-8')
		dict_imei["validity"] = req.POST["validity"].encode('utf-8')
		dict_imei["businessID"] = req.POST["businessID"].encode('utf-8')
		dict_imei["isThirdModel"] = req.POST["isThirdModel"].encode('utf-8')
		dict_imei["mirrtalkCount"] = req.POST["mirrtalkCount"].encode('utf-8')
		dict_imei["mirrtalkInforemarks"] = req.POST["mirrtalkInforemarks"].encode('utf-8')
		dict_imei["mirrtalkHistoryremarks"] = req.POST["mirrtalkHistoryremarks"].encode('utf-8')

		dict_imei["clientIP"] = req.POST["clientIP"].encode('utf-8')

		tmp_appkey = appKey
		tmp_secret = secret

		dict_imei['sign'] = get_sign(dict_imei, tmp_appkey , tmp_secret)
		request_msg = dict_to_str(dict_imei)

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
		
		if object_data["ERRORCODE"] and object_data["ERRORCODE"] != "0":
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "result_msg":result_msg })
		# -----------------------------是否为新建model---------------------------------------
		dict_model = {}
		dict_model["model"] = req.POST["model"].encode('utf-8')
		dict_model["accountID"] = req.POST["accountID"].encode('utf-8')

		# 判断是否需要设置开机参数
		dict_model['sign'] = get_sign(dict_model, tmp_appkey , tmp_secret)

		uri = "accountapi/v2/getCustomArgs"
		request_msg = dict_to_str(dict_model)

		try:
			result_msg = http_post_api(req , uri, request_msg, api_host, api_port )
			object_data = json.loads(result_msg)
		except :
			print result_msg
			pass

		if not object_data :
			result_msg = "http error!"
			return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "result_msg":result_msg })
			pass
		if object_data["ERRORCODE"] and object_data["ERRORCODE"] != "0" :
			return render_to_response(api_html, {'form':form,  "api_name":api_name, "api_action": api_action ,  "api_account": req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
		# # -----------------------------设置开机参数------------------------------------------------
		isnewModel = object_data["RESULT"][0]['isnewModel']
		# isdefine =  object_data["RESULT"][0]['isDefine']
		# 设置开机参数
		dict_set_args = {}
		dict_set_args["model"] = req.POST["model"].encode('utf-8')
		dict_set_args["domain"] = req.POST["domain"].encode('utf-8')
		dict_set_args["customArgs"] = req.POST["customArgs"].encode('utf-8')
		dict_set_args["remark"] = req.POST["remark"].encode('utf-8')
		dict_set_args["accountID"] = req.POST["accountID"].encode('utf-8')
		# 是否设置开机参数
		setArgs = req.POST["setArgs"].encode('utf-8')

		if setArgs == '1' or isnewModel == 1:
			if isnewModel == 1 and len(dict_set_args["accountID"]) != 10 :
				dict_set_args["model"] = req.POST["model"].encode('utf-8')
				dict_set_args["domain"] = 's9c0.mirrtalk.com'  # 线下默认设置
				dict_set_args["customArgs"] = '{"voiceCommand":false,"groupVoice":true,"autoSend":false,"ktvMode":false,"stopNewStatus":false,"stopNewStatusDis":10,"autoSetVolume":"true"}'
			
			dict_set_args['sign'] = get_sign(dict_set_args, tmp_appkey, tmp_secret)

			uri = "accountapi/v2/setCustomArgs"
			request_msg = dict_to_str(dict_set_args)

			try:
				result_msg = http_post_api(req , uri, request_msg, api_host, api_port )
				object_data = json.loads(result_msg)
			except :
				print result_msg
				pass

			if not object_data:
				result_msg = "http error!"
				return render_to_response(api_html, {'form':form, "api_name":api_name, "api_action": api_action , "result_msg":result_msg })
				pass
			else:
				return render_to_response(api_html, {'form':form,  "api_name":api_name, "api_action":api_action , "api_account":req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )
		else:
			return render_to_response(api_html, {'form':form,  "api_name":api_name, "api_action":api_action , "api_account":req.session['accountID'] , "uri": uri,  "request_msg":request_msg, "result_msg":result_msg, "object_data":object_data } )	
	else:
		form = template_form()
		return render_to_response(api_html,{'form':form,  "api_name":api_name, "api_action":api_action , "api_account": req.session['accountID'] })


# class classBusinessRegisterInfo(forms.Form):
# 	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	businessName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	returnType = forms.ChoiceField( choices = REWARD_RETURN_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	parentID = forms.ChoiceField( choices = REWARD_PARENT_ID, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	isChannel = forms.ChoiceField( choices = REWARD_IS_CHANNEL, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	receiverName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverPhone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverAddress = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	allowExchange = forms.ChoiceField( choices = REWARD_ALLOW_EXCHANGE, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	bonusType = forms.ChoiceField( choices = REWARD_BONUS_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	shareInfo = forms.ChoiceField( choices = REWARD_SHARE_INFO, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	bonusReturnTarget = forms.ChoiceField( choices = REWARD_BONUS_RETURN_TARGET_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	userBonusMax = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	businessBonusMax = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	bonusReturnMonth = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
# 	#creatimei
# 	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	isThirdModel = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	mirrtalkCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	mirrtalkInforemarks = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
# 	mirrtalkHistoryremarks = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
# 	clientIP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"127.0.0.1"}) )


# def businessRegisterInfo(req):
# 	api_uri = "rewardapi/v2/businessRegisterInfo"
# 	return templateApp_creat_imei(req, classBusinessRegisterInfo, api_uri , sys._getframe().f_code.co_name, "生成IMEI" )

class classQuickCreateImei(forms.Form):
	#creatimei
	company = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "企业名称" )
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }  ) , label = "设备model")
	businessID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }), label = "企业ID编号")
	isThirdModel = forms.ChoiceField( choices = IS_THIRD_MODEL, widget = forms.Select(attrs={'class':'form-control'} ), label = "model类型" )
	# useType = forms.ChoiceField( choices = USE_TYPE, widget = forms.Select(attrs={'class':'form-control'} ), label = "应用类型" )
	clientappKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "应用标识" )
	mirrtalkCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "生产设备数" )
	clientIP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }  ), label = "本机IP地址" )
	brandType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }  ), label = "品牌名称" )
	mirrtalkInforemarks = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } )  , label = "生产备注")
	mirrtalkHistoryremarks = forms.ChoiceField( choices = MIRRTALK_HISTORY_REMARKS, widget = forms.Select(attrs={'class':'form-control'} ), label = "生产历史备注" )

def quickCreateImei(req):
	api_uri = "accountapi/v2/quickCreateImei"
	return templateApp(req, classQuickCreateImei, api_uri , sys._getframe().f_code.co_name, "生成设备终端号" )

#获取用户自定义参数
class classGetCustomArgs(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "账户"  )
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }), label = "设备model" )

def getCustomArgs(req):
	api_uri = "accountapi/v2/getCustomArgs"
	return templateApp(req, classGetCustomArgs, api_uri , sys._getframe().f_code.co_name ,"获取开机参数")

#设置用户自定义参数
class classUserConfigInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "账户"  )
	domain = forms.ChoiceField( choices = DOMAIN_ADDRE, widget = forms.Select(attrs={'class':'form-control'} ), label = "服务器域名" )
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "设备model" )
	customArgs = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "开机参数"  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "备注信息"  )

def userConfigInfo(req):
	api_uri = "accountapi/v2/setCustomArgs"
	return templateApp(req, classUserConfigInfo, api_uri , sys._getframe().f_code.co_name, "设置开机参数" )

class classSetCustomArgs(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "账户" )
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "设备model" )
	domain = forms.ChoiceField( choices = DOMAIN_ADDRE, widget = forms.Select(attrs={'class':'form-control'} ), label = "服务器域名" )
	customArgs = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "开机信息"  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "备注" )
 
def setCustomArgs(req):
	api_uri = "accountapi/v2/setCustomArgs"
	return templateApp(req, classSetCustomArgs, api_uri , sys._getframe().f_code.co_name, "设置开机参数" )

