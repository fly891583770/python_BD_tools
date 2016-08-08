#!/usr/bin/python
#-*- coding: UTF-8 -*- 

from django.template import loader,Context
from django.http import HttpResponse
from tools.models import modtools
from django.forms import *
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from tools.def_tmp import *


import hashlib
import urllib
import urllib2
import httplib 

import sys
import json
import string

#=====================SEND MESSAGE BEGIN ==================

WEIBO_POI_TYPE =(
	('1','1--综合地理信息'),
	('2','2--综合点加半径'),
	('3','3--路径'),
	('4','4--地理区域'),
	('5','5--整条路'),
)

WEIBO_RECEIVE_SELF =(
	('0','0--不接收'),
	('1','1--接收'),
)

WEIBO_CHECK_TOKENCODE =(
	('0','0--不检查'),
	('1','1--检查'),
)

# skipChannelAuthorize = 1 				---- 跳过频道验证
SKIP_CHANNEL_AUTHORIZE = (
	('0','0--不跳过频道验证'),
	('1','1--跳过频道验证'),
)

#=====================SEND WEIBO END======================
def del_null_str(adict):
	items = adict.items()
	for key,value in items:
		if value == "" :
			del adict[key]


#====================SEND WEIBO BEGIN=======================

class classSendMultimediaPersoanlWeibo(forms.Form):
	receiverAccountID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"接收者accountID"})  )
	interval= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':600,'placeholder':"微博有效时长"})  )
	checkTokenCode= forms.ChoiceField( choices =WEIBO_CHECK_TOKENCODE, widget = forms.Select(attrs={'class':'form-control'} ) )
	level= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"微博的优先级"})  )
	content = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
	multimediaURL= forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
	senderLongitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"发送者经度"})  )
	senderLatitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"发送者纬度"})  )
	senderAltitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"发送者海拔"})  )
	senderDirection= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"发送者有效方向角"})  )
	senderSpeed= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"发送者有效的速度"})  )
	receiverLongitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"终端有效经度"})  )
	receiverLatitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"终端有效纬度"})  )
	receiverDistance= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"终端有效海拔"})  )
	receiverDirection= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"终端有效方向角"})  )
	receiverSpeed= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"终端接收速度"})  )
	callbackURL = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
	commentID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"评论或吐槽的文件编号，长度为32位"})  )
	sourceID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':"外部数据源，长度为32位"})  )
	geometryType= forms.ChoiceField( choices = WEIBO_POI_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )


def sendMultimediaPersonalWeibo(req):
	api_uri = "weiboapi/v2/sendMultimediaPersonalWeibo"
	return templateApp_weibo(req, classSendMultimediaPersoanlWeibo, api_uri , sys._getframe().f_code.co_name, "apiform_normal.html" ,before_sign = del_null_str,request_type = "forms" )

# class classSendMultimediaGroupWeibo(forms.Form):
# 	groupID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiveSelf = forms.ChoiceField( choices = WEIBO_RECEIVE_SELF, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	interval= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':600})  )
# 	level= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	skipChannelAuthorize = forms.ChoiceField( choices =SKIP_CHANNEL_AUTHORIZE, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	content = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
# 	multimediaURL= forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
# 	senderAccountID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderLongitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderLatitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderDirection= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderSpeed= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderAltitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverLongitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverLatitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverDistance= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverDirection= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverSpeed= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	callbackURL = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
# 	commentID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	sourceID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

# def sendMultimediaGroupWeibo(req):
# 	api_uri = "weiboapi/v2/sendMultimediaGroupWeibo"
# 	return templateApp_weibo(req, classSendMultimediaGroupWeibo, api_uri , sys._getframe().f_code.co_name, "apiform_normal.html" ,before_sign = del_null_str, request_type = "forms" )



# class classSendMultimediaOnlineCityWeibo(forms.Form):
# 	receiveSelf = forms.ChoiceField( choices = WEIBO_RECEIVE_SELF, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	interval= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':600})  )
# 	level= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	multimediaURL= forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
# 	multimediaFile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','type':"file"}) )
# 	senderAccountID= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderLongitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderLatitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderDirection= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderSpeed= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	senderAltitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverLongitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverLatitude= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverDistance= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverDirection= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	receiverSpeed= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	callbackURL = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','cols':100,'rows':3} )  )
# 	regionCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
# 	checkTokenCode= forms.ChoiceField( choices =WEIBO_CHECK_TOKENCODE, widget = forms.Select(attrs={'class':'form-control'} ) )
# 	receiveCrowd = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )


# def sendMultimediaOnlineCityWeibo(req):
# 	api_uri = "/weiboapi/v2/sendMultimediaOnlineCityWeibo"
# 	return templateApp_weibo(req, classSendMultimediaOnlineCityWeibo, api_uri , sys._getframe().f_code.co_name, "apiform_normal.html" ,before_sign = del_null_str, request_type = "forms" )


#====================SEND WEIBO END=========================
