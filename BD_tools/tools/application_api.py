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



#---- 群聊频道开放类型
DEVICE_TYPE = (
	('1','1--model'),
	('2','2--IMEI'),
)

class classSetDeviceChannelInfo(forms.Form):
	deviceType =  forms.ChoiceField( choices = DEVICE_TYPE , widget=forms.Select(attrs={'class':'form-control' } ), label = "设备类型")
	deviceName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "设备名")
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "频道编号")
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "备注")

def setDeviceChannelInfo(req):
	api_uri = "/applicationapi/v2/setDeviceChannelInfo"
	return templateApp(req, classSetDeviceChannelInfo, api_uri , sys._getframe().f_code.co_name ,"设置设备默认频道", api_html = "apiform.html")

class classFetchDeviceChannelInfo(forms.Form):
	deviceType =  forms.ChoiceField( choices = DEVICE_TYPE , widget=forms.Select(attrs={'class':'form-control' } ), label = "设备类型")
	deviceName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "设备名")
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,  'value':"1" } ) , label = "分页起始页" )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,  'value':"20"} ) , label = "每页项数" )

def fetchDeviceChannelInfo(req):
	api_uri = "/applicationapi/v2/fetchDeviceChannelInfo"
	return templateApp(req, classFetchDeviceChannelInfo, api_uri , sys._getframe().f_code.co_name ,"查询设备默认频道", api_html = "apiform.html")


