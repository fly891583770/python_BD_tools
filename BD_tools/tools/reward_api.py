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

#donatedType
#1为金钱,2为里程
REWARD_DONATED_TYPE = (
	('1','1--金钱'),
	('2','2--里程'),
)

#regularDonation
#0为否,1为每月自动捐赠,2每季度自动捐赠,3每年自动捐赠
REWARD_REGULAR_DONATION = (
	('0','0--否'),
	('1','1--每月自动捐赠'),
	('2','2--每季自动捐赠'),
	('3','3--每年自动捐赠'),
)

#type
#排名类型１代表日排名，２代表周排名，３代表月>排名，４代表总排名(若type为４则time可以不传)
REWARD_TYPE = (
	('1','1--日排名'),
	('2','2--周排名'),
	('3','3--月排名'),
	('4','4--总排名'),
)

#withdrawType
#1:支付宝提现,2:手机话费充值,3:企业帐户提现(目前只能为1,2,3)
REWARD_WITHDRAW_TYPE = (
	('1','1--支付宝提现'),
	('2','2--手机话费充值'),
	('3','3--企业帐户提现'),
)

#withdrawAccountType
#1代表支付宝提现,2代表手机话费充值(目前只能为1,2)
REWARD_WITHDRAW_ACCOUNT_TYPE = (
	('1','1--支付宝提现'),
	('2','2--手机话费充值'),
)

#showType
#展示类型(默认为1，表示显示给普通用户查看，2表示显示给高级用户)
REWARD_WITHDRAW_ACCOUNT_TYPE = (
	('1','1--显示给普通用户'),
	('2','2--显示给高级用户'),
)

#moneyType
#1：获取密点类型，空：实际金额(其他报错)
REWARD_WITHDRAW_ACCOUNT_TYPE = (
	('1','1--获取密点类型'),
	('','空--实际金额'),
)

#消息类型
SECRET_MESSAGE_TYPE = (
	('','----全部消息'),
	('0','0----未处理'),
	('1','1----同意'),
	('2','2----拒绝'),
)

AMOUNT_TYPE = (
	('1','1----密点'),
	('3','3----保险预购金'),
	('4','4----企业资金'),
)

FROZEN_AMOUNT = (
	('0','0----正常'),
	('1','1----冻结'),
)
#使用类型。1:企业用户,2:开发者用户,3:其他',
USE_TYPE = (
	('2','2----开发者用户'),
)
#===============REWARD END====================



#=====================================reward begin======================================================

class classAddDepositInfo(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  ) 
	depositPassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','value':"123456"})  ) 

def addDepositInfo(req):
	api_uri = "rewardapi/v2/addDepositInfo"
	return templateApp(req, classAddDepositInfo, api_uri , sys._getframe().f_code.co_name )

class classUserFinanceConsume(forms.Form):
	expenseAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	incomeAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	MEPoints = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	WEPoints = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	businessID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	tradeNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	changedType = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	callbackURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def userFinanceConsume(req):
	api_uri = "rewardapi/v2/userFinanceConsume"
	return templateApp(req, classUserFinanceConsume, api_uri , sys._getframe().f_code.co_name )

class classGetBusinessInfo(forms.Form):
	businessName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' }), label = "企业名称", )

def getBusinessInfo(req):
	api_uri = "getBusinessInfo"
	return user_info(req,classGetBusinessInfo, api_uri, sys._getframe().f_code.co_name, "查询企业数据信息")

class classBusinessRegisterInfo(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "用户注册账户"  )
	mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "用户电话" )
	businessName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "企业注册名称" )
	# returnType = forms.ChoiceField( choices = REWARD_RETURN_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# parentID = forms.CharField( widget = forms.TextInput(attrs={'class':'form-control'} ) )
	# isChannel = forms.ChoiceField( choices = REWARD_IS_CHANNEL, widget = forms.Select(attrs={'class':'form-control'} ) )
	receiverName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "收货人名称"  )
	receiverPhone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "收货人电话"   )
	receiverAddress = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "收货人地址"  )
	# allowExchange = forms.ChoiceField( choices = REWARD_ALLOW_EXCHANGE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# bonusType = forms.ChoiceField( choices = REWARD_BONUS_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# shareInfo = forms.ChoiceField( choices = REWARD_SHARE_INFO, widget = forms.Select(attrs={'class':'form-control'} ) )
	# bonusReturnTarget = forms.ChoiceField( choices = REWARD_BONUS_RETURN_TARGET_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# userBonusMax = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	# businessBonusMax = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	# bonusReturnMonth = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "企业信息备注" )

def businessRegisterInfo(req):
	api_uri = "rewardapi/v2/businessRegisterInfo"
	return templateApp(req, classBusinessRegisterInfo, api_uri , sys._getframe().f_code.co_name ,"企业注册", api_html = "apimodel.html")

class classBusinessRegisterInfo_IO(forms.Form):
	# username = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "用户注册账户"  )
	# mobile = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "用户电话" )
	businessName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "企业名称" )
	# returnType = forms.ChoiceField( choices = REWARD_RETURN_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# parentID = forms.CharField( widget = forms.TextInput(attrs={'class':'form-control'} ) )
	# isChannel = forms.ChoiceField( choices = REWARD_IS_CHANNEL, widget = forms.Select(attrs={'class':'form-control'} ) )
	# receiverName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "收货人名称"  )
	# receiverPhone = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "收货人电话"   )
	# receiverAddress = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}), label = "收货人地址"  )
	# allowExchange = forms.ChoiceField( choices = REWARD_ALLOW_EXCHANGE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# bonusType = forms.ChoiceField( choices = REWARD_BONUS_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# shareInfo = forms.ChoiceField( choices = REWARD_SHARE_INFO, widget = forms.Select(attrs={'class':'form-control'} ) )
	# bonusReturnTarget = forms.ChoiceField( choices = REWARD_BONUS_RETURN_TARGET_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	# userBonusMax = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	# businessBonusMax = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	# bonusReturnMonth = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}) , label = "企业信息备注" )

def businessRegisterInfo_IO(req):
	api_uri = "rewardapi/v2/businessRegisterInfo"
	return templateApp(req, classBusinessRegisterInfo_IO, api_uri , sys._getframe().f_code.co_name ,"企业注册", api_html = "apimodel.html")


#=====
class classDonateDaoke(forms.Form):
	donatorAccountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	donatorName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	isAnonymous = forms.ChoiceField( choices = REWARD_IS_ANONYMOUS, widget = forms.Select(attrs={'class':'form-control'} ) )
	amount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	donatedType = forms.ChoiceField( choices = REWARD_DONATED_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	regularDonation = forms.ChoiceField( choices = REWARD_REGULAR_DONATION, widget = forms.Select(attrs={'class':'form-control'} ) )

def donateDaoke(req):
	api_uri = "rewardapi/v2/donateDaoke"
	return templateApp(req, classDonateDaoke , api_uri, sys._getframe().f_code.co_name)

class classFetchDonationInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	startTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	startPage =	forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"1" })  )
	pageCount =	forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"20" })  )


def fetchDonationInfo(req):
	api_uri = "rewardapi/v2/fetchDonationInfo"
	return templateApp(req, classFetchDonationInfo , api_uri, sys._getframe().f_code.co_name)

class classGetAllRankInfo(forms.Form):
	time = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	type = forms.ChoiceField( choices = REWARD_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	startRank = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	endRank = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"1"})  )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"20"})  )

def getAllRankInfo(req):
	api_uri = "rewardapi/v2/getAllRankInfo"
	return templateApp(req, classGetAllRankInfo , api_uri, sys._getframe().f_code.co_name)

class classGetRewardRank(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	time = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	type = forms.ChoiceField( choices = REWARD_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def getRewardRank(req):
	api_uri = "rewardapi/v2/getRewardRank"
	return templateApp(req, classGetRewardRank , api_uri, sys._getframe().f_code.co_name)

class classGetAllWithdrawInfo(forms.Form):
	withdrawType = forms.ChoiceField( choices = REWARD_WITHDRAW_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def getAllWithdrawInfo(req):
	api_uri = "rewardapi/v2/getAllWithdrawInfo"
	return templateApp(req, classGetAllWithdrawInfo , api_uri, sys._getframe().f_code.co_name)

class classTransferEnterpriseAccount(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	businessID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	receiptID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAmount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def transferEnterpriseAccount(req):
	api_uri = "rewardapi/v2/transferEnterpriseAccount"
	return templateApp(req, classTransferEnterpriseAccount , api_uri, sys._getframe().f_code.co_name)

class classTransferOwnAccount(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	receiptID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAmount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccountType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def transferOwnAccount(req):
	api_uri = "rewardapi/v2/transferOwnAccount"
	return templateApp(req, classTransferOwnAccount , api_uri, sys._getframe().f_code.co_name)

class classGetBalanceDetail(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	startTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"1"})  )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"20"})  )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def getBalanceDetail(req):
	api_uri = "rewardapi/v2/getBalanceDetail"
	return templateApp(req, classGetBalanceDetail , api_uri, sys._getframe().f_code.co_name)

class classFetchDepositHistory(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	startTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	startPage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"1"})  )
	pageCount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control',  'value':"20"})  )
	showType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	isAll = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def fetchDepositHistory(req):
	api_uri = "rewardapi/v2/fetchDepositHistory"
	return templateApp(req, classFetchDepositHistory , api_uri, sys._getframe().f_code.co_name)

class classGetUserDepositInfo(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	showType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def getUserDepositInfo(req):
	api_uri = "rewardapi/v2/getUserDepositInfo"
	return templateApp(req, classGetUserDepositInfo , api_uri, sys._getframe().f_code.co_name)

class classGetRewardAmountByMileage(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	mileage = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def getRewardAmountByMileage(req):
	api_uri = "rewardapi/v2/getRewardAmountByMileage"
	return templateApp(req, classGetRewardAmountByMileage , api_uri, sys._getframe().f_code.co_name)

class classCrashRecharge(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	changedAmount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	businessID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	endTime = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def crashRecharge(req):
	api_uri = "rewardapi/v2/crashRecharge"
	return templateApp(req, classCrashRecharge , api_uri, sys._getframe().f_code.co_name)

class classApplyWithdrawDeposit(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	depositPassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	applyWithdrawAmount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	autoWithdraw = forms.ChoiceField( choices = REWARD_IS_ANONYMOUS, widget = forms.Select(attrs={'class':'form-control'} ) )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def applyWithdrawDeposit(req):
	api_uri = "rewardapi/v2/applyWithdrawDeposit"
	return templateApp(req, classApplyWithdrawDeposit , api_uri, sys._getframe().f_code.co_name)

class classApplyWithdrawMoney(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	daokePassword = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	applyWithdrawAmount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccountType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	callbackURL = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	tradeNumber = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def applyWithdrawMoney(req):
	api_uri = "rewardapi/v2/applyWithdrawMoney"
	return templateApp(req, classApplyWithdrawMoney , api_uri, sys._getframe().f_code.co_name)

class classGetUserFinanceInfo(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	moneyType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )

def getUserFinanceInfo(req):
	api_uri = "rewardapi/v2/getUserFinanceInfo"
	return templateApp(req, classGetUserFinanceInfo , api_uri, sys._getframe().f_code.co_name)

class classTransferOwnAccount(forms.Form):
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control' } ) , label = "accountID")
	receiptID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAmount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccount = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )
	withdrawAccountType = forms.ChoiceField( choices = REWARD_WITHDRAW_ACCOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ) )
	remark = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def transferOwnAccount(req):
	api_uri = "rewardapi/v2/transferOwnAccount"
	return templateApp(req, classTransferOwnAccount , api_uri, sys._getframe().f_code.co_name)


class classConfirmCancelContract(forms.Form):
	IMEI = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'})  )

def confirmCancelContract(req):
	api_uri = "rewardapi/v2/confirmCancelContract"
	return templateApp(req, classConfirmCancelContract , api_uri, sys._getframe().f_code.co_name)

class classUserMoneyFrozen(forms.Form): 
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control','placeholder':'批量操作账户，需要以逗号分隔'} ) , label = "用户账号") 
	moneyType = forms.ChoiceField( choices = AMOUNT_TYPE, widget = forms.Select(attrs={'class':'form-control'} ), label = "资金类型" )
	isFrozenAmount = forms.ChoiceField( choices = FROZEN_AMOUNT, widget = forms.Select(attrs={'class':'form-control'} ), label = "冻结状态" )

def userMoneyFrozen(req):
	api_uri = "rewardapi/v2/userMoneyFrozen"
	return templateApp(req, classUserMoneyFrozen , api_uri, sys._getframe().f_code.co_name,"账户资金冻结", api_html = "apimodel.html")

class classQueryDeviceStatus(forms.Form):
	IMEIs = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control'})  ) 

def queryDeviceStatus(req):
	api_uri = "rewardapi/v2/queryDeviceStatus"
	return templateApp(req, classQueryDeviceStatus, api_uri , sys._getframe().f_code.co_name, "查询设备状态" )

class classAddUserAppkeyInfo(forms.Form): 
	useType = forms.ChoiceField( choices = USE_TYPE, widget = forms.Select(attrs={'class':'form-control'} ),label= "使用类型"   )
	accountID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "道客账户" )
	businessID = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "企业编号"  )
	appName = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "应用名称" )
	appLogo = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label = "应用图标URL" )
	website = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control'}),label= "网站"  )

def addUserAppkeyInfo(req):
	api_uri = "rewardapi/v2/addUserAppkeyInfo"
	return templateApp(req, classAddUserAppkeyInfo , api_uri, sys._getframe().f_code.co_name,"添加appKey")

#=====================================reward end======================================================
