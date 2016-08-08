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



#================OAUTH BEGIN===============

#第三方开发者类型
DEVELOPER_TYPE = (
	('1','1--外部普通开发者'),
)

#设置开发者审核状态
DEVELOPER_STATUS = (
	('0','0--审核中'),
	('1','1--审核通过'),
	('2','2--无开发权限')
)

#设置第三方应用审核状态
THIRD_PARTY_APP_STATUS = (
	('0','0--审核中'),
	('1','1--审核通过'),
	('2','2--审核未通过')
)

#获取开发者审核状态
GET_DEVELOPER_TYPE = (
	('','所有'),
	('0','0--审核中'),
	('1','1--审核通过'),
	('2','2--无开发权限')
)

#获取开发者的第三方应用
VALIDITY_TYPE = (
	('','所有'),
	('0','0--无效'),
	('1','1--有效'),
)

#设置APP频率控制FreqType
OAUTH_FREQUENCY_TYPE = (
	('','暂时支持第一种'),
	('1','1--每小时/每天/每月/每年'),
	('2','2--包年/包月'),
)

#暂不支持
OAUTH_NOT_SUPPORT_NOW = (
	('','暂时不支持'),
)

#设置APP频率控制customType
OAUTH_CUSTOM_TYPE = (
	('1','1--每年'),
	('2','2--每月'),
	('3','3--每天'),
	('4','4--每小时'),
)


#OAUTH第三方开发者类型(对应appKeyInfo)
#1:内部用户,2:企业用户,3:个人用户,4:合同用户
OAUTH_DEVELOPER_TYPE = (
	('1','1--内部用户'),
	('2','2--企业用户'),
	('3','3--个人用户(需要accountID)'),
	('4','4--合同用户'),
)

#===============OAUTH END=====================







#=====================================oauth begin======================================================
#开发者相关API





#第三方开发者注册身份信息
class classRegisterIdentityInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "道客账号" )
	developerType = forms.ChoiceField( choices = DEVELOPER_TYPE, widget = forms.Select(attrs={'class':'form-control'}), label = "开发者类型")
	developerName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="开发者名称")
	province = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="开发者所在省份")
	city = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="开发者所在城市")
	address = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="详细地址")
	postcode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="邮编")
	email = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="邮箱")
	phone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="联系电话")
	website = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="网站")
	emergencyContactName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="紧急联系人姓名")
	emergencyContactPhone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="紧急联系人电话")
	IDCardPictureURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="身份证图片存放地址")
	businessLicensePictureURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="营业执照图片存放地址")
	taxRegistrationPictureURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="税务登记图片存放地址")
	organizationCodePictureURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label ="组织机构代码图片存放地址")

def registerIdentityInfo(req):
	api_uri = "oauth/v2/registerIdentityInfo"
	return templateApp(req, classRegisterIdentityInfo, api_uri , sys._getframe().f_code.co_name,"第三方开发者注册身份信息","apiform.html")

#合并到registerIdentityInfo
# class classDeveloperIdAdd(forms.Form):
# 	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
# 	developerType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	IDCardPicture = forms.ImageField()  
# 	businessLicensePicture = forms.ImageField()  
# 	taxRegistrationPicture = forms.ImageField()  
# 	organizationCodePicture = forms.ImageField()

# def developerIdAdd(req):
# 	api_uri = "oauth/v2/developerIdAdd"
# 	return templateApp(req, classDeveloperIdAdd, api_uri , sys._getframe().f_code.co_name)

#管理后台审核开发者状态
class classManageDeveloperStatus(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "道客账号" )
	developerType = forms.ChoiceField( choices = DEVELOPER_TYPE, widget = forms.Select(attrs={'class':'form-control'}),label = "开发者类型")
	status = forms.ChoiceField( choices = DEVELOPER_STATUS, widget = forms.Select(attrs={'class':'form-control'}),label= "审核状态")

def manageDeveloperStatus(req):
	api_uri = "oauth/v2/manageDeveloperStatus"
	return templateApp(req, classManageDeveloperStatus, api_uri , sys._getframe().f_code.co_name,"后台审核开发者状态")

#获取开发者资料
class classGetDeveloperInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )

def getDeveloperInfo(req):
	api_uri = "oauth/v2/getDeveloperInfo"
	return templateApp(req, classGetDeveloperInfo, api_uri , sys._getframe().f_code.co_name)

#更新开发者资料
class classUpdateIdentityInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	province = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	city = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	address = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	postcode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	email = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	phone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	website = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	emergencyContactName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	emergencyContactPhone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def updateIdentityInfo(req):
	api_uri = "oauth/v2/updateIdentityInfo"
	return templateApp(req, classUpdateIdentityInfo, api_uri , sys._getframe().f_code.co_name)

#管理后台获取开发者信息
class classManageDeveloperInfo(forms.Form):
	status = forms.ChoiceField( choices = GET_DEVELOPER_TYPE, widget = forms.Select(attrs={'class':'form-control'}))
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"1" } ))
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"20" } ))
	startTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def manageDeveloperInfo(req):
	api_uri = "oauth/v2/manageDeveloperInfo"
	return templateApp(req, classManageDeveloperInfo, api_uri , sys._getframe().f_code.co_name)

#第三方开发者应用管理
#获取appKey信息
class classGetAppKeyInfo(forms.Form):
	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getAppKeyInfo(req):
	api_uri = "oauth/v2/getAppKeyInfo"
	return templateApp(req, classGetAppKeyInfo, api_uri , sys._getframe().f_code.co_name)

#生成新应用
class classCreateNewApp(forms.Form):
	developerType = forms.ChoiceField( choices = OAUTH_DEVELOPER_TYPE, widget = forms.Select(attrs={'class':'form-control'}))
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	name = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	website = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	appLogo = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def createNewApp(req):
	api_uri = "oauth/v2/createNewApp"
	return templateApp(req, classCreateNewApp, api_uri , sys._getframe().f_code.co_name)

#审核第三方应用状态
class classManageAppStatus(forms.Form):
	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ),label= "认证appKey")
	status = forms.ChoiceField( choices = THIRD_PARTY_APP_STATUS, widget = forms.Select(attrs={'class':'form-control'}),label="审核状态")
	reasonRejection = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ),label="驳回原因")

def manageAppStatus(req):
	api_uri = "oauth/v2/manageAppStatus"
	return templateApp(req, classManageAppStatus, api_uri , sys._getframe().f_code.co_name,"审核第三方appKey状态")


#获取开发者的应用信息，输入参数为appKey,sign,accountID,validity
class classGetDeveloperAppInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	validity = forms.ChoiceField( choices = VALIDITY_TYPE, widget = forms.Select(attrs={'class':'form-control'}))

def getDeveloperAppInfo(req):
	api_uri = "oauth/v2/getDeveloperAppInfo"
	return templateApp(req, classGetDeveloperAppInfo, api_uri , sys._getframe().f_code.co_name)

#开发者申请提升应用等级appKey,sign,accountID,clientAppKey,appliedLevel
# class classApplyRaiseAppLevel(forms.Form):
# 	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
# 	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	appliedLevel = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

# def applyRaiseAppLevel(req):
# 	api_uri = "oauth/v2/applyRaiseAppLevel"
# 	return templateApp(req, classApplyRaiseAppLevel, api_uri , sys._getframe().f_code.co_name)

# #管理后台获取所有应用等级变更信息appKey,sign,status,startPage,pageCount,startTime,endTime.
# class classManageAppLevelChangeInfo(forms.Form):
# 	status = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	startTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

# def manageAppLevelChangeInfo(req):
# 	api_uri = "oauth/v2/manageAppLevelChangeInfo"
# 	return templateApp(req, classManageAppLevelChangeInfo, api_uri , sys._getframe().f_code.co_name)

# #管理后台更改应用等级appKey,sign,clientAppKey,level
# class classManageAppChangeLevel(forms.Form):
# 	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	level = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

# def manageAppChangeLevel(req):
# 	api_uri = "oauth/v2/manageAppChangeLevel"
# 	return templateApp(req, classManageAppChangeLevel, api_uri , sys._getframe().f_code.co_name)

#设置OAUTH授权频次控制
class classSetAppFreqInfo(forms.Form):
	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	apiName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	frequencyType = forms.ChoiceField( choices = OAUTH_FREQUENCY_TYPE, widget = forms.Select(attrs={'class':'form-control'}))
	customType = forms.ChoiceField( choices = OAUTH_CUSTOM_TYPE, widget = forms.Select(attrs={'class':'form-control'}))
	requestCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	#暂时不支持
	# startTime = forms.ChoiceField( choices = OAUTH_NOT_SUPPORT_NOW, widget = forms.Select(attrs={'class':'form-control'}))
	# endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def setAppFreqInfo(req):
	api_uri = "oauth/v2/setAppFreqInfo"
	return templateApp(req, classSetAppFreqInfo, api_uri , sys._getframe().f_code.co_name)	

#获取OAUTH授权频次控制
class classGetAppFreqInfo(forms.Form):
	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	apiName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getAppFreqInfo(req):
	api_uri = "oauth/v2/getAppFreqInfo"
	return templateApp(req, classGetAppFreqInfo, api_uri , sys._getframe().f_code.co_name)

#更新OAUTH授权频次控制
class classUpdateAppFreqInfo(forms.Form):
	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	apiName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	frequencyType = forms.ChoiceField( choices = OAUTH_FREQUENCY_TYPE, widget = forms.Select(attrs={'class':'form-control'}))
	customType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	requestCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	# startTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	# endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def updateAppFreqInfo(req):
	api_uri = "oauth/v2/updateAppFreqInfo"
	return templateApp(req, classUpdateAppFreqInfo, api_uri , sys._getframe().f_code.co_name)		

#授权认证
# class classGetAuthCode(forms.Form):
# 	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
# 	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	redirectURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	scope = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

# def getAuthCode(req):
# 	api_uri = "oauth/v2/getAuthCode"
# 	return templateApp(req, classGetAuthCode, api_uri , sys._getframe().f_code.co_name)

# class classGetAccessToken(forms.Form):
# 	code = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
# 	redirectURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	grantType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

# def getAccessToken(req):
# 	api_uri = "oauth/v2/getAccessToken"
# 	return templateApp(req, classGetAccessToken, api_uri , sys._getframe().f_code.co_name)

# class classRefreshAccessToken(forms.Form):
# 	refreshToken =  forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	redirectURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
# 	grantType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

# def refreshAccessToken(req):
# 	api_uri = "oauth/v2/refreshAccessToken"
# 	return templateApp(req, classRefreshAccessToken, api_uri , sys._getframe().f_code.co_name)

class classGetPasswordToken(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	redirectURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	scope = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	grantType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getPasswordToken(req):
	api_uri = "oauth/v2/getPasswordToken"
	return templateApp(req, classGetPasswordToken, api_uri , sys._getframe().f_code.co_name)

class classGetImplicitToken(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	clientAppKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	redirectURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	scope = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	grantType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getImplicitToken(req):
	api_uri = "oauth/v2/getImplicitToken"
	return templateApp(req, classGetImplicitToken, api_uri , sys._getframe().f_code.co_name)

#trust
class classGetTrustAuthCode(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	scope = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"userInfo,realTimeInfo,collectInfo,drivingInfo,weibo,reward,bindmirrtalk" } ))

def getTrustAuthCode(req):
	api_uri = "oauth/v2/getTrustAuthCode"
	return templateApp(req, classGetTrustAuthCode, api_uri , sys._getframe().f_code.co_name)

class classGetTrustAccessCode(forms.Form):
	code = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	grantType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':'authorizationCode' } ))
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	scope = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"userInfo,realTimeInfo,collectInfo,drivingInfo,weibo,reward,bindmirrtalk"  } ))

def getTrustAccessCode(req):
	api_uri = "oauth/v2/getTrustAccessCode"
	return templateApp(req, classGetTrustAccessCode, api_uri , sys._getframe().f_code.co_name)

class classRefreshTrustAccessToken(forms.Form):
	refreshToken = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	grantType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def refreshTrustAccessToken(req):
	api_uri = "oauth/v2/refreshTrustAccessToken"
	return templateApp(req, classRefreshTrustAccessToken, api_uri , sys._getframe().f_code.co_name)

class classGetScopeInfo(forms.Form):
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"1" } ))
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"20" } ))

def getScopeInfo(req):
	api_uri = "oauth/v2/getScopeInfo"
	return templateApp(req, classGetScopeInfo, api_uri , sys._getframe().f_code.co_name)
#=====================================oauth end======================================================