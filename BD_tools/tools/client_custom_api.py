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



#---- 获取频道类型 
FETCH_SECRET_INFO_TYPE = (
	('1', '1--群聊频道广场'),
	('2', '2--已创建的频道'),
	('3', '3--已加入的频道'),
	('4', '4--等待验证/驳回的频道')
)

#---- 频道类别
SECRET_CATALOG_LIST = (
	('','----全部'),
	('300001','300001--的哥的姐'),
	('300002','300002--汽车之家'),
	('300003','300003--星座天文'),
	('300004','300004--电影小说'),
	('300005','300005--闲聊八卦'),
	('300006','300006--搞笑段子'),
	('300007','300007--清唱一句'),
	('301010','301010--同事朋友'),
	('301011','301011--车友会'),
	('301012','301012--同城交友'),
	('301013','301013--兴趣爱好'),
	('301014','301014--行业交流'),
	('301015','301015--吃喝玩乐'),
	('301016','301016--品牌产品'),
	('301017','301017--线下服务'),
	('301018','301018--交通出行'),
	('301019','301019--应急救援'),
	('301020','301020--两性情感'),
	('301021','301021--地区频道')

)
#--微频道
MIC__CATALOG_LIST = (
	('','----全部'),
	('100101','100101--同事朋友'),
	('100102','100102--车友会'),
	('100103','100103--同城交友'),
	('100104','100104--兴趣爱好'),
	('100105','100105--行业交流'),
	('100106','100106--吃喝玩乐'),
	('100107','100107--品牌产品'),
	('100108','100108--线下服务'),
	('100109','100109--交通出行'),
	('100110','100110--应急救援'),
	('100111','100111--两性情感'),
	('100112','100112--地区频道'),
	('200001','200001--节操几个钱'),
	('200002','200002--美女要不要'),
	('200003','200003--大叔也疯狂'),
	('200004','200004--鲜肉来两斤'),
	('200005','200005--旅行约一约'),
	('200007','200007--美食胖子送'),
	('200008','200008--搞基自由行'),

)

JOIN_CHANNEL_STATUS = (
	('0','0--等待验证的频道'),
	('2','2--管理员拒绝的频道'),
)


#---- 群聊频道开放类型
SECRET_OPENTYPE = (
	('0','0--非公开'),
	('1','1--公开'),
)

#---- 群聊频道加入类型
SECRET_VERITY_TYPE = (
	('0','0--加入不需要验证'),
	('1','1--加入需求验证'),
)

SECRET_VERITY_QUERY = (
	('','--全部'),
	('0','0--加入不需要验证'),
	('1','1--加入需求验证'),
)

#---- 群聊频道审核类型
SECRET_CHECKSTATUS_TYPE = (
	('1','1--通过'),
	('2','2--拒绝'),
)
#---- 获取用户状态
SECRET_USER_STATUS = (
	('1','1--正常'),
	('2','2--禁言'),
	('3','3--拉黑')

)
#---- 设置关联键
SECRET_USERKEY = (
	('4','4--+键'),
	('5','5--++键')

)

#---- 管理频道类型
MANAGE_SECRET_TYPE = (
	('1','1--公司管理频道(curStatus  2 关闭频道)'),
	('2','2--管理员管理频道(curStatus 1-正常 / 2-禁言用户/3-拉黑用户)')
)

#---- 按键类型
SECRET_CUSTOMTYPE = (
	('2','2--customType:2(actionType:5)'),
	('6','6--customType:6(actionType:4)')
)

#得到在线列表
FETCH_SECRET_ONLINE_INFO = (
	('','可不传，自动识别普通用户或管理员'),
	('1','1--管理员得到在线列表'),
	('2','2--普通用户得到在线列表')
)

#频道类型
GET_CHANNEL_TYPE = (

	('1','1--主播频道'),
	('2','2--群聊频道')
)
#====================MicroChannel==========
#频道状态
MICROCHANNEL_STATUS = (
	('0','0--未审核'),
	('1','1--驳回'),
	('2','2--成功')
)
#查询频道类型
FETCH_MICRO_TYPE = (
	('0','0--公司查询频道'),
	('1','1--频道管理员查询频道'),
	('2','2--普通用户查询频道')

 )
#修改微频道/被驳回的频道
MODIFY_CHANNEL_TYPE = (
	('1','1--修改未通过的频道微'),
	('2','2--修改已通过的频道微')
)

FOLLOW_CHANNEL_TYPE = (
	('1',"1--关注频道"),
	('2',"2--解散频道")
)

#消息类型
SECRET_MESSAGE_TYPE = (
	('','----全部消息'),
	('0','0----未处理'),
	('1','1----同意'),
	('2','2----拒绝'),
)

SHUTUP_STATUS = (
	('1',"1--禁言"),
	('0',"0--不禁言"),
)

#频道分类有效性分类
CHANNEL_VALIDITY_TYPE = (
    ('0','0--关闭'),
    ('1','1--开启'),
)

#频道类型
GET_CHANNEL_TYPE = (
	('1','1--主播频道'),
	('2','2--群聊频道')
)
#================MIC END===================

class classGetCatalogInfo(forms.Form):
	channelType = forms.ChoiceField( choices = GET_CHANNEL_TYPE, widget = forms.Select(attrs={'class':'form-control'}) , label = "频道类型" )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,  'value':"1" } ) , label = "分页起始页" )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,  'value':"20"} ) , label = "每页项数" )

def getChannelCatalog(req):
	api_uri = "clientcustom/v2/getCatalogInfo"
	return templateApp(req, classGetCatalogInfo, api_uri , sys._getframe().f_code.co_name,"查询频道分类", api_html = "apiform.html")

#增加频道分类
class classAddChannelCatalog(forms.Form):
	catalogName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) ,label = "频道分类名" )
	introduction = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "介绍" )
	catalogType = forms.ChoiceField( choices = GET_CHANNEL_TYPE, widget = forms.Select(attrs={'class':'form-control'}),label = "频道类型")
	validity = forms.ChoiceField( choices = CHANNEL_VALIDITY_TYPE ,  widget=forms.Select(attrs={'class':'form-control'}) , label = "是否有效")
	sortIndex = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) ,label = "排序索引" )
	logoURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) ,label = "logo链接" )

def addChannelCatalog(req):
	api_uri = "/clientcustom/v2/addChannelCatalog"
	return templateApp(req, classAddChannelCatalog, api_uri , sys._getframe().f_code.co_name, "增加频道分类", api_html = "apiform.html" )

#修改频道分类
class classModifyChannelCatalog(forms.Form):
	catalogID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) ,label = "频道分类号" )
	catalogName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "频道分类名" )
	introduction = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "介绍" )
	validity = forms.ChoiceField( choices = CHANNEL_VALIDITY_TYPE ,  widget=forms.Select(attrs={'class':'form-control'}),label = "是否有效" )
	sortIndex = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "排序索引" )
	logoURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "logo链接" )


def modifyChannelCatalog(req):  
    api_uri = "clientcustom/v2/modifyChannelCatalog"
    return templateApp(req, classModifyChannelCatalog, api_uri , sys._getframe().f_code.co_name, "修改频道分类", api_html = "apiform.html" )


#  转移频道{{ field.label }}
class classTransferSecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "管理员账号" ) 
	password = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "管理员密码")
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "频道编号")
	receiverAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "接受者账号")

def transferSecretChannel(req):
	api_uri = "clientcustom/v2/transferSecretChannel"
	return templateApp(req, classTransferSecretChannel, api_uri , sys._getframe().f_code.co_name, "频道转移", api_html = "apimodel.html" )

class classUserShutUp(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "账户编号" ) 
	totalTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  , label = "禁言时间(秒)" )
	status = forms.ChoiceField( choices=SHUTUP_STATUS, widget=forms.Select(attrs={'class':'form-control'}), label = "禁言状态" )

def userShutUp(req):
	api_uri = "clientcustom/v2/userShutUp"
	return templateApp(req, classUserShutUp, api_uri , sys._getframe().f_code.co_name, "用户禁言", api_html = "apiform.html" )

class classFetchUserShutUpInfo(forms.Form):
	accountIDs = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "账户编号" ) 
	count = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"1"}) ,label = "查询数" )

def fetchUserShutUpInfo(req):
	api_uri = "clientcustom/v2/fetchUserShutUpInfo"
	return templateApp(req, classFetchUserShutUpInfo, api_uri , sys._getframe().f_code.co_name, "禁言查询", api_html = "apiform.html" )

class classApplySecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" ) 
	channelName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelIntroduction = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelCityCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelCatalogID = forms.ChoiceField( choices = SECRET_CATALOG_LIST, widget = forms.Select(attrs={'class':'form-control'} ) )
	channelCatalogUrl = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	openType = forms.ChoiceField( choices = SECRET_OPENTYPE , widget = forms.Select(attrs={'class':'form-control'})  )
	isVerify = forms.ChoiceField( choices = SECRET_VERITY_TYPE ,  widget=forms.Select(attrs={'class':'form-control'})  )
	channelKeyWords = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def applySecretChannel(req):
	api_uri = "clientcustom/v2/applySecretChannel"
	return templateApp(req, classApplySecretChannel, api_uri , sys._getframe().f_code.co_name)


class classModifySecretChannelInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" ) 
	channelName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelOpenType = forms.ChoiceField( choices = SECRET_OPENTYPE , widget = forms.Select(attrs={'class':'form-control'})  )
	channelIsVerify  = forms.ChoiceField( choices = SECRET_VERITY_TYPE ,  widget=forms.Select(attrs={'class':'form-control'})  )
	channelIntro = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelCatalogID = forms.ChoiceField( choices = SECRET_CATALOG_LIST, widget = forms.Select(attrs={'class':'form-control'} ) )
	channelLogoUrl = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelCitycode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelKeyWords = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )


def modifySecretChannelInfo(req):
	api_uri = "clientcustom/v2/modifySecretChannelInfo"
	return templateApp(req, classModifySecretChannelInfo, api_uri , sys._getframe().f_code.co_name)




class classManageSecretChannelUsers(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" ) 
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	infoType = forms.ChoiceField(choices=MANAGE_SECRET_TYPE  , widget = forms.Select(attrs={'class':'form-control'}   ) )
	userAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' })  ) 
	curStatus = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def manageSecretChannelUsers(req):
	api_uri = "clientcustom/v2/manageSecretChannelUsers"
	return templateApp(req, classManageSecretChannelUsers, api_uri , sys._getframe().f_code.co_name)


class classFetchSecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	channelName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ) )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ))
	cityCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ))
	isVerify = forms.ChoiceField( choices = SECRET_VERITY_QUERY ,  widget=forms.Select(attrs={'class':'form-control'})  )
	catalogID = forms.ChoiceField( choices = SECRET_CATALOG_LIST, widget = forms.Select(attrs={'class':'form-control'} ) )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"1" } ))
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"20" } ))


def fetchSecretChannel(req):
	api_uri = "clientcustom/v2/fetchSecretChannel"
	return templateApp(req, classFetchSecretChannel, api_uri , sys._getframe().f_code.co_name)


class classSecretMessage(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	status = forms.ChoiceField(choices=SECRET_MESSAGE_TYPE  , widget = forms.Select(attrs={'class':'form-control'}   ) )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"1" } ))
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"20" } ))


def secretChannelMessage(req):
	api_uri = "clientcustom/v2/secretChannelMessage"
	return templateApp(req, classSecretMessage, api_uri , sys._getframe().f_code.co_name)


class classVeritySecretChannelMessage(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	applyAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ) )
	applyAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ) )
	checkRemark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ) )
	checkStatus = forms.ChoiceField( choices = SECRET_CHECKSTATUS_TYPE,  widget=forms.Select(attrs={'class':'form-control'} ) )
	applyIdx = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ) )


def veritySecretChannelMessage(req):
	api_uri = "clientcustom/v2/veritySecretChannelMessage"
	return templateApp(req, classVeritySecretChannelMessage, api_uri , sys._getframe().f_code.co_name)


class classJoinSecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	uniqueCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	remark  = forms.CharField( max_length = "120", widget=forms.TextInput(attrs={'class':'form-control'} ))


def joinSecretChannel(req):
	api_uri = "clientcustom/v2/joinSecretChannel"
	return templateApp(req, classJoinSecretChannel, api_uri , sys._getframe().f_code.co_name)


class classGetSecretChannelInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def getSecretChannelInfo(req):
	api_uri = "clientcustom/v2/getSecretChannelInfo"
	return templateApp(req, classGetSecretChannelInfo, api_uri , sys._getframe().f_code.co_name)

class classGetUserJoinListSecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	infoType = forms.ChoiceField( choices = FETCH_SECRET_ONLINE_INFO, widget = forms.Select(attrs={'class':'form-control'} ) )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"1" } ))
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' , 'value':"20" } ))

def getUserJoinListSecretChannel(req):
	api_uri = "clientcustom/v2/getUserJoinListSecretChannel"
	return templateApp(req, classGetUserJoinListSecretChannel, api_uri , sys._getframe().f_code.co_name)


class classQuitSecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def quitSecretChannel(req):
	api_uri = "clientcustom/v2/quitSecretChannel"
	return templateApp(req, classQuitSecretChannel, api_uri , sys._getframe().f_code.co_name)

# 解散频道
class classDissolveSecretChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" ) 
	password = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def dissolveSecretChannel(req):
	api_uri = "clientcustom/v2/dissolveSecretChannel"
	return templateApp(req, classDissolveSecretChannel, api_uri , sys._getframe().f_code.co_name)


#=====================================主播频道 begin==========================================

class classApplyMicroChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "账户编号" ) 
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "频道编号" )
	channelName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "频道名称" )
	channelIntroduction = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "频道简介" )
	channelCityCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "城市编号"  )
	channelCatalogID = forms.ChoiceField( choices = MIC__CATALOG_LIST, widget = forms.Select(attrs={'class':'form-control'} ) , label = "类型编号")
	channelCatalogUrl = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "logUrl" )
	chiefAnnouncerIntr = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "主播简介" )
	channelKeyWords = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "关键字" )

def applyMicroChannel(req):
	api_uri = "clientcustom/v2/applyMicroChannel"
	return templateApp(req, classApplyMicroChannel, api_uri , sys._getframe().f_code.co_name,"申请主播频道")

class classCheckApplyMicroChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" )
	checkAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) ) 
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	checkRemark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	checkStatus = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelRemark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	applyIdx = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelKeyWords = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def checkApplyMicroChannel(req):
	api_uri = "clientcustom/v2/checkApplyMicroChannel"
	return templateApp(req, classCheckApplyMicroChannel, api_uri , sys._getframe().f_code.co_name)



class classFetchMicroChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" )
	channelStatus = forms.ChoiceField( choices = MICROCHANNEL_STATUS, widget = forms.Select(attrs={'class':'form-control'} ) )
	cityCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	catalogID = forms.ChoiceField( choices = MIC__CATALOG_LIST, widget = forms.Select(attrs={'class':'form-control'} ) )
	channelName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelKeyWords = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"1"})  )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':'20'})  )
	infoType = forms.ChoiceField( choices = FETCH_MICRO_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def fetchMicroChannel(req):
	api_uri = "clientcustom/v2/fetchMicroChannel"
	return templateApp(req, classFetchMicroChannel, api_uri , sys._getframe().f_code.co_name)


class classGetMicroChannelInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )


def getMicroChannelInfo (req):
	api_uri = "clientcustom/v2/getMicroChannelInfo "
	return templateApp(req, classGetMicroChannelInfo, api_uri , sys._getframe().f_code.co_name)

class classModifyMicroChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" )
	channelCityCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelCatalogID = forms.ChoiceField( choices = MIC__CATALOG_LIST, widget = forms.Select(attrs={'class':'form-control'} ) )
	channelName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelKeyWords = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	infoType = forms.ChoiceField( choices = MODIFY_CHANNEL_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	channelIntroduction = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	beforeChannelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	chiefAnnouncerIntr = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	channelCatalogUrl = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )


def modifyMicroChannel(req):
	api_uri = "clientcustom/v2/modifyMicroChannel"
	return templateApp(req, classModifyMicroChannel, api_uri , sys._getframe().f_code.co_name)


class classFollowMicroChannel(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	uniqueCode 	= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	followType =  forms.ChoiceField( choices = FOLLOW_CHANNEL_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )



def followMicroChannel  (req):
	api_uri = "clientcustom/v2/followMicroChannel"
	return templateApp(req, classFollowMicroChannel, api_uri , sys._getframe().f_code.co_name)

# 批量关注微频道 2015-05-21 
class classBatchFollowMicroChannel(forms.Form):
	uniqueCode = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "邀请码"   )
	totalList = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control'}) , label = "用户列表,使用逗号分隔(一次拉粉最多只能一千个)"  )

def batchFollowMicroChannel(req):
	api_uri = "clientcustom/v2/batchFollowMicroChannel"
	return templateApp_Batch(req, classBatchFollowMicroChannel, api_uri , sys._getframe().f_code.co_name, "批量关注微频道", api_html = "apiform.html" )

# 批量关注微频道 2015-05-21 

class classGetBossFollowList(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }) , label = "accountID" )
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})   )
	startPage 	= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"1"})   )
	pageCount =  forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"20"})   )



def getBossFollowListMicroChannel(req):
	api_uri = "clientcustom/v2/getBossFollowListMicroChannel"
	return templateApp(req, classGetBossFollowList, api_uri , sys._getframe().f_code.co_name)




#===========================主播频道 end========================================================


#=====================================clientcustom begin======================================================


class classSetSubscribeMsg(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	subParameter = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def setSubscribeMsg(req):
	api_uri = "clientcustom/v2/setSubscribeMsg"
	return templateApp(req, classSetSubscribeMsg, api_uri , sys._getframe().f_code.co_name )

class classResetInviteUniqueCode(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	channelNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))
	channelType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ))

def resetInviteUniqueCode(req):
	api_uri = "clientcustom/v2/resetInviteUniqueCode"
	return templateApp(req, classResetInviteUniqueCode, api_uri , sys._getframe().f_code.co_name )


#=====================================clientcustom end======================================================




#====================================weme setting begin================================
# 判断用户是否在线
class classCheckIsOnline(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )

def checkIsOnline(req):
	api_uri = "clientcustom/v3/checkIsOnline"
	return templateApp(req, classCheckIsOnline, api_uri , sys._getframe().f_code.co_name ,api_html = "apiform_ex.html"  )


#==================================
# 获取用户按键 2015-05-22 
class classGetUserkeyInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	actionType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )

def getUserkeyInfo(req):
	api_uri = "clientcustom/v2/getUserkeyInfo"
	return templateApp(req, classGetUserkeyInfo, api_uri , sys._getframe().f_code.co_name )

# 设置用户按键 2015-05-22

class classSetUserkeyInfo(forms.Form):
	tmp_parameter = '''{"count":"3",
"list": [{	"actionType":"3","customType":"10",
			"customParameter":""
		},
		{	"actionType":"4","customType":"10",
			"customParameter":"000000153"
		},
		{	"actionType":"5","customType":"10",
			"customParameter":"000000153"
		}]
}'''

	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "accountID" )
	# initial  初始化值 
	parameter = forms.CharField(initial= tmp_parameter , widget=forms.Textarea(attrs={'class':'form-control','cols':800} ) )

def setUserkeyInfo(req):
	api_uri = "clientcustom/v2/setUserkeyInfo"
	return templateApp(req, classSetUserkeyInfo, api_uri , sys._getframe().f_code.co_name )

#====================================weme setting end


#---------------------------map api ===begin===================================================================

class classUpdatePOIAttr(forms.Form):
	ID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	NM = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	ST = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	TP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	BD = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	LD = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	DP = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	TT = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )

def updatePOIAttr(req):
	api_uri = "mapapi/v2/updatePOIAttr"
	return templateApp(req, classUpdatePOIAttr, api_uri , sys._getframe().f_code.co_name )
#---------------------------map api ====end====================================================================


#------------------------------------ main debug add  api  ========begin===========================
#获取用户自定义参数
class classGetCustomArgs(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "账户"  )
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }), label = "设备model" )

def getCustomArgs(req):
	api_uri = "accountapi/v2/getCustomArgs"
	return templateApp(req, classGetCustomArgs, api_uri , sys._getframe().f_code.co_name ,"获取用户自定义参数", api_html = "apimodel.html")

#设置用户自定义参数
class classUserConfigInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "账户"  )
	domain = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "域名"  ) 
	model = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }), label = "设备model" )
	customArgs = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "开机参数"  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ), label = "备注信息"  )

def userConfigInfo(req):
	api_uri = "accountapi/v2/setCustomArgs"
	return templateApp(req, classUserConfigInfo, api_uri , sys._getframe().f_code.co_name, "设置用户自定义参数", api_html = "apimodel.html" )

class classSetAppKeySecret(forms.Form):
	appKey = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	secret = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def setAppKeySecret(req):
	api_uri = ""
	return templateApp_Debug(req, classSetAppKeySecret, api_uri  , sys._getframe().f_code.co_name )

class classDevicePowerOn(forms.Form):
	imei = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	imsi = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	mod = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def devicePowerOn(req):
	api_uri = "config"
	return templateApp(req, classDevicePowerOn, api_uri  , sys._getframe().f_code.co_name )	
#------------------------------------ main debug add  api  ========end===========================


#------------------------------------ dfs  api  ========end===========================


class classTxtToVoice(forms.Form):
	text = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def txtToVoice(req):
	api_uri = "dfsapi/v2/txt2voice"
	return templateApp(req, classTxtToVoice, api_uri , sys._getframe().f_code.co_name )

#------------------------------------ dfs  api  ========end===========================



#------------------------------------ web  api  ========end===========================
class classSendSms(forms.Form):
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	content= forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' ,'value':"短信测试信息"}) )
	platform = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	is_times = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
def sendSms(req):
	api_uri = "webapi/v2/sendSms"
	return templateApp(req, classSendSms, api_uri , sys._getframe().f_code.co_name )
#------------------------------------ web  api  ========end===========================



#---------------------------------------serverChannel ---begin

class classGetCustomDefineInfo(forms.Form):
	defineName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	actionType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"1"}) )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"20"}) )

def getCustomDefineInfo(req):
	api_uri = "clientcustom/v2/getCustomDefineInfo"
	return templateApp(req, classGetCustomDefineInfo, api_uri , sys._getframe().f_code.co_name )
#---------------------------------------serverChannel ---begin


class classTTSDemo(forms.Form):
	text = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'} ) )
	
def TTSDemo(req):
	api_uri = "dfsapi/v2/txt2voice"
	return templateApp(req, classTTSDemo, api_uri , sys._getframe().f_code.co_name)


