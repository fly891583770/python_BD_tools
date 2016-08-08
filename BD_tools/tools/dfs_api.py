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


#======================== DFS BEGIN =======================#
#灵云jtt 文本转amr音频文件
class classJtxt2voice(forms.Form):
	text = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def jtxt2voice(req):
	api_uri = "/dfsapi/v2/jtxt2voice"
	return templateApp(req,classJtxt2voice,api_uri,sys._getframe().f_code.co_name,"灵云jtt 文本转amr音频文件")

#保存文件
class classSaveFile(forms.Form):
	fileType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )	
	filePath = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','type':"file"})  )
	retry = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )	
def saveFile(req):
	api_uri = "dfsapi/v2/savefile"
	return template_save_file(req, classSaveFile , api_uri, sys._getframe().f_code.co_name, "上传文件",api_html = "apiform_upload.html", request_type = "forms" )
