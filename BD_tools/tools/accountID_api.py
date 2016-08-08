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

import hashlib
import urllib
import urllib2
import httplib 

import sys
import json
import string

#coding:utf-8






#=====================================道客账户 begin======================================================

def add_custom_before_sign(dict):
	if dict['accountType'] == "1":
		del dict['mobile']
		del dict['userEmail']
	elif dict['accountType'] == "2":
		del dict['username']
		del dict['userEmail']
	elif dict['accountType'] == "3":
		del dict['username']
		del dict['mobile']

# 1代表用户名为主,2代表手机号码为主,3代表邮箱为主
REGISTER_ACCOUNT_TYPE = (
	('1','1--用户名'),
	('2','2--手机号码'),
	('3','3--邮箱'),
)

# def api_function(dict):
# 	if dict['loginType'] == "1":
# 		del dict['QQ']
# 		del dict['Email']
# 		del dict['MSN']
# 		del dict['weixin']
# 		del dict['sinaweibo']
# 		del dict['KLD']
# 	elif dict['loginType'] == "2":
# 		del dict['QQ']
# 		del dict['mobile']
# 		del dict['MSN']
# 		del dict['weixin']
# 		del dict['sinaweibo']
# 		del dict['KLD']
# 	elif dict['loginType'] == "3":
# 		del dict['Email']
# 		del dict['mobile']
# 		del dict['MSN']
# 		del dict['weixin']
# 		del dict['sinaweibo']
# 		del dict['KLD']
# 	elif dict['loginType'] == "4":
# 		del dict['Email']
# 		del dict['mobile']
# 		del dict['QQ']
# 		del dict['weixin']
# 		del dict['sinaweibo']
# 		del dict['KLD']
# 	elif dict['loginType'] == "5":
# 		del dict['Email']
# 		del dict['mobile']
# 		del dict['QQ']
# 		del dict['MSN']
# 		del dict['sinaweibo']
# 		del dict['KLD']
# 	elif dict['loginType'] == "6":
# 		del dict['Email']
# 		del dict['mobile']
# 		del dict['QQ']
# 		del dict['weixin']
# 		del dict['MSN']
# 		del dict['KLD']
# 	elif dict['loginType'] == "7":
# 		del dict['Email']
# 		del dict['mobile']
# 		del dict['QQ']
# 		del dict['weixin']
# 		del dict['sinaweibo']
# 		del dict['MSN']

#1手机号码登录；2用户邮箱登陆；3QQ登录；4MSN登录；5微信登陆；6新浪微博;7第三方信任账户
LOGIN_TYPE = (
	('1','1--手机号码登录'),
	('2','2--邮箱登陆'),
	('3','3--QQ登录'),
	('4','4--MSN登录'),
	('5','5--微信登陆'),
	('6','6--新浪微博'),
	('7','7--第三方信任账户'),
)

# def api_function(dict):
# 	if dict['gender'] == "1":
# 		del dict['Female']
# 		del dict['Neutral']
# 	elif dict['gender'] == "2":
# 		del dict['man']
# 		del dict['Neutral']
# 	elif dict['gender'] == "3":
# 		del dict['man']
# 		del dict['Female']

# 1男,2女,3中性
GENDER_TYPE = (
	('1','1--男'),
	('2','2--女'),
	('3','3--中性'),
)

# def api_function(dict):
# 	if dict['numberType'] == "0":
# 		del dict['talk_key']
# 		del dict['Sound_record']
# 	elif dict['numberType'] == "1":
# 		del dict['number']
# 		del dict['Sound_record']
# 	elif dict['numberType'] == "4":
# 		del dict['number']
# 		del dict['talk_key']

# 0表示两个号码,1代表吐槽键,4代表录音键
NUMBER_TYPE = (
	('0','0--两个号码'),
	('1','1--吐槽键'),
	('4','4--录音键'),
)


# def api_function(dict):
# 	if dict['numberType'] == "0":
# 		del dict['one']
# 		del dict['four']
# 	elif dict['numberType'] == "1":
# 		del dict['all']
# 		del dict['four']
# 	elif dict['numberType'] == "4":
# 		del dict['all']
# 		del dict['one']

#0表示两个号码都恢复默认值；1表示一号键callcenter恢复默认值；4，表示四号键sos恢复默认
NUMBER_TYPE = (
	('0','0--两个号码都恢复默认值'),
	('1','1--一号键callcenter恢复默认值'),
	('4','4--四号键sos恢复默认'),
)



#创建道客帐户
class classAddCustomAccount(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label ="用户名" ) 
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ),label ="手机号码")
	userEmail = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ),label ="用户邮箱")
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ),label ="账户密码")
	accountType = forms.ChoiceField( choices = REGISTER_ACCOUNT_TYPE , widget=forms.Select(attrs={'class':'form-control' } ),label ="注册方式")
	nickname = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ),label ="用户昵称")

def addCustomAccount(req):
	api_uri = "accountapi/v2/addCustomAccount"
	return templateApp(req, classAddCustomAccount, api_uri , sys._getframe().f_code.co_name, "创建道客帐户",before_sign = add_custom_before_sign)

#IMEI预入库
class classApiPrestroge(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def apiPrestroge(req):
	api_uri = "accountapi/v2/apiPrestroge"
	return templateApp(req, classApiPrestroge, api_uri , sys._getframe().f_code.co_name)

#绑定第三方账户与语镜账号
class classAssociateAccountWithAccountID(forms.Form):
	#accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	account = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	loginType = forms.ChoiceField( choices = LOGIN_TYPE ,widget = forms.Select(attrs = {'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def associateAccountWithAccountID(req):
	api_uri = "accountapi/v2/associateAccountWithAccountID"
	return templateApp(req, classAssociateAccountWithAccountID, api_uri , sys._getframe().f_code.co_name)

#判断IMEI是否允许绑定
class classCheckImei(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def checkImei(req):
	api_uri = "accountapi/v2/checkImei"
	return templateApp(req, classCheckImei, api_uri , sys._getframe().f_code.co_name)

#检查用户是否绑定IMEI
class classCheckIsBindImei(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def checkIsBindImei(req):
	api_uri = "accountapi/v2/checkIsBindImei"
	return templateApp(req, classCheckIsBindImei, api_uri , sys._getframe().f_code.co_name)

#用户登陆
class classCheckLogin(forms.Form):
	# accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	clientIP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"127.0.0.1" } )) 
def checkLogin(req):
	api_uri = "accountapi/v2/checkLogin"
	return templateApp(req, classCheckLogin, api_uri , sys._getframe().f_code.co_name)

#判断是否允许注册
class classCheckRegistration(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def checkRegistration(req):
	api_uri = "accountapi/v2/checkRegistration"
	return templateApp(req, classCheckRegistration, api_uri , sys._getframe().f_code.co_name)

#解绑imei
class classDisconnectAccount(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def disconnectAccount(req):
	api_uri = "accountapi/v2/disconnectAccount"
	return templateApp(req, classDisconnectAccount, api_uri , sys._getframe().f_code.co_name)

#更新用户资料
class classFixUserInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	nickname = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	userEmail = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	gender = forms.ChoiceField( choices = GENDER_TYPE , widget = forms.Select(attrs = {'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def fixUserInfo(req):
	api_uri = "accountapi/v2/fixUserInfo"
	return templateApp(req, classFixUserInfo, api_uri , sys._getframe().f_code.co_name)

#添加第三方帐户
class classGenerateDaokeAccount(forms.Form):
	account = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	loginType = forms.ChoiceField( choices = LOGIN_TYPE ,widget = forms.Select(attrs = {'class':'form-control' } ))
	nickname = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def generateDaokeAccount(req):
	api_uri = "accountapi/v2/generateDaokeAccount"
	return templateApp(req, classGenerateDaokeAccount, api_uri , sys._getframe().f_code.co_name)

#通过第三方帐户得到账户编号
class classGetAccountIDByAccount(forms.Form):
	account = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	loginType = forms.ChoiceField( choices = LOGIN_TYPE ,widget = forms.Select(attrs = {'class':'form-control' } ))
	clientIP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"127.0.0.1" } ))

def getAccountIDByAccount(req):
	api_uri = "accountapi/v2/getAccountIDByAccount"
	return templateApp(req, classGetAccountIDByAccount, api_uri , sys._getframe().f_code.co_name)

#通过手机号码得到帐户编号
class classGetAccountIDFromMobile(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getAccountIDFromMobile(req):
	api_uri = "accountapi/v2/getAccountIDFromMobile"
	return templateApp(req, classGetAccountIDFromMobile, api_uri , sys._getframe().f_code.co_name)

#获取用户自定义参数
class classGetCustomArgs(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getCustomArgs(req):
	api_uri = "accountapi/v2/getCustomArgs"
	return templateApp(req, classGetCustomArgs, api_uri , sys._getframe().f_code.co_name)

#得到IMEI和手机号
class classGetImeiPhone(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getImeiPhone(req):
	api_uri = "accountapi/v2/getImeiPhone"
	return templateApp(req, classGetImeiPhone, api_uri , sys._getframe().f_code.co_name)

#得到终端信息
class classGetMirrtalkInfoByImei(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getMirrtalkInfoByImei(req):
	api_uri = "accountapi/v2/getMirrtalkInfoByImei"
	return templateApp(req, classGetMirrtalkInfoByImei, api_uri , sys._getframe().f_code.co_name)

#得到手机验证码
class classGetMobileVerificationCode(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	# content = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getMobileVerificationCode(req):
	api_uri = "accountapi/v2/getMobileVerificationCode"
	return templateApp(req, classGetMobileVerificationCode, api_uri , sys._getframe().f_code.co_name)

#得到用户自定义号码
class classGetUserCustomNumber(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	numberType = forms.ChoiceField( choices = NUMBER_TYPE ,widget = forms.Select(attrs = {'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getUserCustomNumber(req):
	api_uri = "accountapi/v2/getUserCustomNumber"
	return templateApp(req, classGetUserCustomNumber, api_uri , sys._getframe().f_code.co_name)

#得到用户资料
class classGetUserInfo(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getUserInfo(req):
	api_uri = "accountapi/v2/getUserInfo"
	return templateApp(req, classGetUserInfo, api_uri , sys._getframe().f_code.co_name)

#获取用户信息
class classGetUserInformation(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label= "accountID" )
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getUserInformation(req):
	api_uri = "accountapi/v2/getUserInformation"
	return templateApp(req, classGetUserInformation, api_uri , sys._getframe().f_code.co_name)

#判断帐户是否在线
class classJudgeOnlineAccounJ(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def judgeOnlineAccount(req):
	api_uri = "accountapi/v2/judgeOnlineAccount"
	return templateApp(req, classJudgeOnlineAccounJ, api_uri , sys._getframe().f_code.co_name)

#判断给定手机号是否在线
class classJudgeOnlineMobile(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def judgeOnlineMobile(req):
	api_uri = "accountapi/v2/judgeOnlineMobile"
	return templateApp(req, classJudgeOnlineMobile, api_uri , sys._getframe().f_code.co_name)

#重置用户自定义号码
class classResetUserCustomNumber(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	numberType = forms.ChoiceField( choices = NUMBER_TYPE ,widget = forms.Select(attrs = {'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } )) 

def resetUserCustomNumber(req):
	api_uri = "accountapi/v2/resetUserCustomNumber"
	return templateApp(req, classResetUserCustomNumber, api_uri , sys._getframe().f_code.co_name)

#重置用户道客密码
class classResetUserPassword(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def resetUserPassword(req):
	api_uri = "accountapi/v2/resetUserPassword"
	return templateApp(req, classResetUserPassword, api_uri , sys._getframe().f_code.co_name)

#发送验证URL到邮箱
class classSendVerificationURL(forms.Form):
	userEmail = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	URL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,'value':"https://github.com/jayzh1010"} ))
	content = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,'value':"hellonihao" } ))

def sendVerificationURL(req):
	api_uri = "accountapi/v2/sendVerificationURL"
	return templateApp(req, classSendVerificationURL, api_uri , sys._getframe().f_code.co_name)

#设置用户自定义号码
class classSetUserCustomNumber(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	call1Number = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	call2Number = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def setUserCustomNumber(req):
	api_uri = "accountapi/v2/setUserCustomNumber"
	return templateApp(req, classSetUserCustomNumber, api_uri , sys._getframe().f_code.co_name)

#更改用户自定义参数
class classUpdateCustomArgs(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	customArgs = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } )) 

def updateCustomArgs(req):
	api_uri = "accountapi/v2/updateCustomArgs"
	return templateApp(req, classUpdateCustomArgs, api_uri , sys._getframe().f_code.co_name)

#更改用户道客密码
class classUpdateUserPassword(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	oldPassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	newPassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def updateUserPassword(req):
	api_uri = "accountapi/v2/updateUserPassword"
	return templateApp(req, classUpdateUserPassword, api_uri , sys._getframe().f_code.co_name)

#绑定imei
class classUserBindAccountMirrtalk(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def userBindAccountMirrtalk(req):
	api_uri = "accountapi/v2/userBindAccountMirrtalk"
	return templateApp(req, classUserBindAccountMirrtalk, api_uri , sys._getframe().f_code.co_name)

#验证手机或邮箱
class classVerifyEmailOrMobile(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	email = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } )) 

def verifyEmailOrMobile(req):
	api_uri = "accountapi/v2/verifyEmailOrMobile"
	return templateApp(req, classVerifyEmailOrMobile, api_uri , sys._getframe().f_code.co_name)

#车机设备号与道客imei关联
class classAssociateDeviceIDWithImei(forms.Form):
	deviceID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def associateDeviceIDWithImei(req):
	api_uri = "accountapi/v2/associateDeviceIDWithImei"
	return templateApp(req, classAssociateDeviceIDWithImei, api_uri , sys._getframe().f_code.co_name)

#获取用户昵称
class classGetUserData(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	field = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	accessToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getUserData(req):
	api_uri = "accountapi/v2/getUserData"
	return templateApp(req, classGetUserData, api_uri , sys._getframe().f_code.co_name)

# 获取手机号对应的验证码
class classGetDynamicVerifycode(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getDynamicVerifycode(req):
	api_uri = "accountapi/v2/getDynamicVerifycode"
	return templateApp(req, classGetDynamicVerifycode, api_uri , sys._getframe().f_code.co_name)

# 认证新生成的验证码
class classCheckDynamicVerifycode(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	verifyCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
def checkDynamicVerifycode(req):
	api_uri = "accountapi/v2/checkDynamicVerifycode"
	return templateApp(req, classCheckDynamicVerifycode, api_uri , sys._getframe().f_code.co_name)

#手机用户获取密码重置的验证码
class classResetPasswordInitVerifyCode(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def resetPasswordInitVerifyCode(req):
	api_uri = "accountapi/v2/resetPasswordInitVerifyCode"
	return templateApp(req, classResetPasswordInitVerifyCode, api_uri , sys._getframe().f_code.co_name)

#手机用户根据验证码重置新密码
class classResetPasswordCheckVerifyCode(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	verifyCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	newPassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def resetPasswordCheckVerifyCode(req):
	api_uri = "accountapi/v2/resetPasswordCheckVerifyCode"
	return templateApp(req, classResetPasswordCheckVerifyCode, api_uri , sys._getframe().f_code.co_name)
	
#生成IMEI
class classCreateImei(forms.Form):
	company = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	businessID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	isThirdModel = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	clientappKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	mirrtalkCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	clientIP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	mirrtalkInforemarks = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	mirrtalkHistoryremarks = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
def createImei(req):
	api_uri = "accountapi/v2/createImei"
	return templateApp(req, classCreateImei, api_uri , sys._getframe().f_code.co_name)
#=====================================道客账户 end======================================================

#修复昵称
class classRepairNickname(forms.Form):
	imei = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def repairNickname(req):
	api_uri = "crazyapi/v2/autorepairnicknameurl"
	return templateApp_Get(req, classRepairNickname, api_uri , sys._getframe().f_code.co_name,'修复昵称')
