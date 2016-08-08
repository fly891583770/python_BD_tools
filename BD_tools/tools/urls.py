#!/usr/bin/python
#-*- coding: UTF-8 -*-

#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.http import HttpResponse
from tools.accountID_api import *
# import tools.login_ing
# import tools.client_custom_api
# import tools.creat_imei_process
# import tools.disbind_imei_process

from tools.login_ing import *
from tools.oauth_api import *
from tools.client_custom_api import *
from tools.reward_api import *
from tools.creat_imei_process import *
from tools.disbind_imei_process import *
from tools.application_api import *
from tools.weibo_api import *
from tools.dfs_api import *
# from tools.accountID import *

import sys

reload = reload(sys) 
sys.setdefaultencoding('gb18030')


# from django.conf import settings
# if settings.DEBUG is False:
# url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT } ),


urlpatterns = patterns (
			'',
			url(r'^$',login),
			url(r'^login$',login),
			url(r'^logout$',logout),
			url(r'^index$', index),
			url(r'^left$', left),
			url(r'^right$',right),
			url(r'^top$',top),
			#------------------业务---------------------#
			url(r'^getMirrtalkInfoByImei$',getMirrtalkInfoByImei),
			url(r'^getBusinessInfo$',getBusinessInfo),
			url(r'^businessRegisterInfo$',businessRegisterInfo),
			url(r'^userShutUp$',userShutUp),
			url(r'^fetchUserShutUpInfo$',fetchUserShutUpInfo),
			url(r'^setCustomArgs$',setCustomArgs),
			url(r'^transferSecretChannel$',transferSecretChannel),
			url(r'^cancellationAccount$',cancellationAccount),
			url(r'^batchFollowMicroChannel$',batchFollowMicroChannel),
			url(r'^getChannelCatalog$',getChannelCatalog),
			url(r'^addChannelCatalog$',addChannelCatalog),
			url(r'^modifyChannelCatalog$',modifyChannelCatalog),
			url(r'^repairNickname$',repairNickname),

		 	# add by wjy 20150907 businessRegisterInfo_IO
		 	url(r'^businessRegisterInfo_IO$',businessRegisterInfo_IO),
			url(r'^quickCreateImei$',quickCreateImei),
			url(r'^getCustomArgs$',getCustomArgs),
			url(r'^userConfigInfo$',userConfigInfo),

			# add by wjy 20150909 userMoneyFrozen
			# url(r'^getUserMoneyType$',getUserMoneyType),
			# url(r'^userMoneyFrozen$',userMoneyFrozen),

			# add by wjy 20150924 
			#----------------application file ------------begin------------
			url(r'^setDeviceChannelInfo$',setDeviceChannelInfo),
			url(r'^fetchDeviceChannelInfo$',fetchDeviceChannelInfo),
			#----------------application file ------------end------------

			url(r'^queryDeviceStatus$',queryDeviceStatus),

			#----------------微博--------begin
			url(r'^sendMultimediaPersonalWeibo$',sendMultimediaPersonalWeibo),
			# url(r'^sendMultimediaGroupWeibo$',sendMultimediaGroupWeibo),
			# url(r'^sendMultimediaOnlineCityWeibo$',sendMultimediaOnlineCityWeibo),
			#----------------微博--------end

			#------------------dfsapi------------------#
			url(r'^jtxt2voice$',jtxt2voice),
			url(r'^saveFile$',saveFile),

			#------------------end---------------------#

			#------------------end---------------------#
	# 		#------------user secret channel  begin-------------------------
	# 		url(r'^getCatalogInfo$',getCatalogInfo),

			
	# 		url(r'^dissolveSecretChannel$',dissolveSecretChannel),

	# 		url(r'^applySecretChannel$',applySecretChannel),
	# 		url(r'^fetchSecretChannel$',fetchSecretChannel),
	# 		url(r'^secretChannelMessage$',secretChannelMessage),
	# 		url(r'^joinSecretChannel$',joinSecretChannel),
	# 		url(r'^quitSecretChannel$',quitSecretChannel),
	# 		url(r'^veritySecretChannelMessage$',veritySecretChannelMessage),
	# 		url(r'^getSecretChannelInfo$',getSecretChannelInfo),
	# 		url(r'^getUserJoinListSecretChannel$',getUserJoinListSecretChannel),
	# 		url(r'^manageSecretChannelUsers$',manageSecretChannelUsers),
	# 		url(r'^modifySecretChannelInfo$',modifySecretChannelInfo),

	# 		#------------user secret channel  end-------------------------
	# 		url(r'^getCatalogInfo$',getCatalogInfo  ),

	# 		#------------user microChannel begin----------------------------
	# 		url(r'^modifyMicroChannel$',modifyMicroChannel ),
	# 		url(r'^followMicroChannel$',followMicroChannel ),
	# 		url(r'^batchFollowMicroChannel$',batchFollowMicroChannel),
	# 		url(r'^applyMicroChannel$',applyMicroChannel ),
	# 		url(r'^checkApplyMicroChannel$',checkApplyMicroChannel ),
	# 		url(r'^fetchMicroChannel$',fetchMicroChannel ),
	# 		url(r'^getMicroChannelInfo$',getMicroChannelInfo ),
	# 		url(r'^getBossFollowListMicroChannel$',getBossFollowListMicroChannel ),

	# 		# url(r'^getBossFollowListMicroChannel$',getBossFollowListMicroChannel ),
	# 		# url(r'^resetInviteUniqueCode$',resetInviteUniqueCode ),

	# 		#------------user microChannel end------------------------------

			
	# 		#--------------道客账户 begin-------------------------
		
	 		url(r'^addCustomAccount$',addCustomAccount),
	# 		url(r'^apiPrestroge$',apiPrestroge),
	# 		url(r'^associateAccountWithAccountID$',associateAccountWithAccountID),
	# 		url(r'^checkImei$',checkImei),
	# 		url(r'^checkIsBindImei$',checkIsBindImei),
	# 		url(r'^checkLogin$',checkLogin),
	# 		url(r'^checkRegistration$',checkRegistration),
	# 		url(r'^disconnectAccount$',disconnectAccount),
	# 		url(r'^fixUserInfo$',fixUserInfo),
	# 		url(r'^generateDaokeAccount$',generateDaokeAccount),
	# 		url(r'^getAccountIDByAccount$',getAccountIDByAccount),
	# 		url(r'^getAccountIDFromMobile$',getAccountIDFromMobile),
	# 		url(r'^getCustomArgs$',getCustomArgs),
	# 		url(r'^getImeiPhone$',getImeiPhone),
	# 		url(r'^getMirrtalkInfoByImei$',getMirrtalkInfoByImei),
	# 		url(r'^getMobileVerificationCode$',getMobileVerificationCode),
	# 		url(r'^getUserCustomNumber$',getUserCustomNumber),
	# 		url(r'^getUserInfo$',getUserInfo),
	# 		url(r'^getUserInformation$',getUserInformation),
	# 		url(r'^judgeOnlineAccount$',judgeOnlineAccount),
	# 		url(r'^judgeOnlineMobile$',judgeOnlineMobile),
	# 		url(r'^resetUserCustomNumber$',resetUserCustomNumber),
	# 		url(r'^resetUserPassword$',resetUserPassword),
	# 		url(r'^sendVerificationURL$',sendVerificationURL),
	# 		url(r'^setUserCustomNumber$',setUserCustomNumber),
	# 		url(r'^updateCustomArgs$',updateCustomArgs),
	# 		url(r'^updateUserPassword$',updateUserPassword),
	# 		url(r'^userBindAccountMirrtalk$',userBindAccountMirrtalk),
	# 		url(r'^verifyEmailOrMobile$',verifyEmailOrMobile),
	# 		url(r'^associateDeviceIDWithImei$',associateDeviceIDWithImei),
	# 		url(r'^getUserData$',getUserData),
	# 		# url(r'^getOauthVerifycode$',getOauthVerifycode),
	# 		# url(r'^checkOauthVerifycode$',checkOauthVerifycode),
	# 		url(r'^getDynamicVerifycode$',getDynamicVerifycode),
	# 		url(r'^checkDynamicVerifycode$',checkDynamicVerifycode),

	# 		url(r'^resetPasswordInitVerifyCode$',resetPasswordInitVerifyCode),
	# 		url(r'^resetPasswordCheckVerifyCode$',resetPasswordCheckVerifyCode),
	# 		url(r'^createImei$',createImei),
	# 		#--------------道客账户 end-------------------------

	# 		#--------------daoke oauth---------------
	# 		# url(r'^getScopeInfo$',getScopeInfo),
	# 		# url(r'^getTrustAuthCode$',getTrustAuthCode),
	# 		# url(r'^getTrustAccessCode$',getTrustAccessCode),
	# 		# url(r'^refreshTrustAccessToken$',refreshTrustAccessToken),
	# 		#developer
	 		url(r'^registerIdentityInfo$',registerIdentityInfo),
	# 		# url(r'^developerIdAdd$',developerIdAdd),
			url(r'^manageDeveloperStatus$',manageDeveloperStatus),
			url(r'^addUserAppkeyInfo$',addUserAppkeyInfo),
	# 		url(r'^getDeveloperInfo$',getDeveloperInfo),
	# 		url(r'^updateIdentityInfo$',updateIdentityInfo),
	# 		url(r'^manageDeveloperInfo$',manageDeveloperInfo),

	# 		#developer's app
	# 		url(r'^getAppKeyInfo$',getAppKeyInfo),
	# 		url(r'^createNewApp$',createNewApp),
	# 		url(r'^getDeveloperAppInfo$',getDeveloperAppInfo),
	# 		# url(r'^applyRaiseAppLevel$',applyRaiseAppLevel),
	# 		# url(r'^manageAppLevelChangeInfo$',manageAppLevelChangeInfo),
	# 		# url(r'^manageAppChangeLevel$',manageAppChangeLevel),
	# 		url(r'^setAppFreqInfo$',setAppFreqInfo),
	# 		url(r'^getAppFreqInfo$',getAppFreqInfo),
	# 		url(r'^updateAppFreqInfo$',updateAppFreqInfo),
			url(r'^manageAppStatus$',manageAppStatus),
			
	# 		#authrization
	# 		# url(r'^getAuthCode$',getAuthCode),
	# 		# url(r'^getAccessToken$',getAccessToken),
	# 		# url(r'^refreshAccessToken$',refreshAccessToken),
	# 		url(r'^getImplicitToken$',getImplicitToken),
	# 		url(r'^getPasswordToken$',getPasswordToken),

	# 		#oauth for Trust 
	# 		url(r'^getScopeInfo$',getScopeInfo),
	# 		url(r'^getTrustAuthCode$',getTrustAuthCode),
	# 		url(r'^getTrustAccessCode$',getTrustAccessCode),
	# 		url(r'^refreshTrustAccessToken$',refreshTrustAccessToken),

	# 		#--------------daoke oauth---------------

	# 		#-------------clientcustom setting begin---------
	# 		url(r'^setSubscribeMsg$',setSubscribeMsg),
	# 		url(r'^applyMicroChannel$',applyMicroChannel),
	# 		url(r'^checkApplyMicroChannel$',checkApplyMicroChannel),
	# 		url(r'^fetchMicroChannel$',fetchMicroChannel),
	# 		url(r'^followMicroChannel$',followMicroChannel),
	# 		url(r'^resetInviteUniqueCode$',resetInviteUniqueCode),
	# 		url(r'^setSubscribeMsg$',setSubscribeMsg),

	# 		#-------------clientcustom setting end-----------

	# 		#-------------WEME setting begin---------
	# 		url(r'^checkIsOnline$',checkIsOnline),
	# 		url(r'^getUserkeyInfo$',getUserkeyInfo),
	# 		url(r'^setUserkeyInfo$',setUserkeyInfo),
	# 		#-------------WEME setting end-----------

	# 		#------------reward api begin-----------------------
	# 		#--添加押金信息
	# 		url(r'^addDepositInfo$',addDepositInfo),
			
	# 		#--用户捐赠
	# 		url(r'^donateDaoke$',donateDaoke),
	# 		url(r'^fetchDonationInfo$',fetchDonationInfo),
	# 		url(r'^getAllRankInfo$',getAllRankInfo),
	# 		url(r'^getRewardRank$',getRewardRank),
	# 		#--财务打款
	# 		url(r'^getAllWithdrawInfo$',getAllWithdrawInfo),
	# 		url(r'^transferEnterpriseAccount$',transferEnterpriseAccount),
	# 		url(r'^transferOwnAccount$',transferOwnAccount),
	# 		#--用户查询资金
	# 		url(r'^getBalanceDetail$',getBalanceDetail),
	# 		url(r'^fetchDepositHistory$',fetchDepositHistory),
	# 		url(r'^getUserDepositInfo$',getUserDepositInfo),
	# 		url(r'^getRewardAmountByMileage$',getRewardAmountByMileage),
	# 		url(r'^crashRecharge$',crashRecharge),
	# 		#--用户消费
	# 		url(r'^applyWithdrawDeposit$',applyWithdrawDeposit),
	# 		url(r'^applyWithdrawMoney$',applyWithdrawMoney),
	# 		url(r'^getUserFinanceInfo$',getUserFinanceInfo),
	# 		url(r'^transferOwnAccount$',transferOwnAccount),
	# 		url(r'^userFinanceConsume$',userFinanceConsume),
	# 		#--设备取消合约
	# 		url(r'^confirmCancelContract$',confirmCancelContract),
	# 		url(r'^confirmExchangeGoods$',confirmExchangeGoods),
			
	# 		#------------reward api end-----------------------


	# 		#---------------map api-------------------------
	# 		url(r'^updatePOIAttr$',updatePOIAttr),
	# 		#------------------------------------------------

			
	# 		#---------------map api-------------------------
	# 		url(r'^setAppKeySecret$',setAppKeySecret),
	# 		url(r'^userConfigInfo$',userConfigInfo),
	# 		url(r'^devicePowerOn$',devicePowerOn),
			
	# 		#------------------------------------------------

	# 		#---------------dfs api-------------------------
	# 		url(r'^txtToVoice$',txtToVoice),

			
	# 		#------------------------------------------------

	# 		#---------------web api-------------------------
	# 		url(r'^sendSms$',sendSms),

			
	# 		#------------------------------------------------

	# 		#---------server channel ---begin
	# 		url(r'^getCustomDefineInfo$',getCustomDefineInfo),
	# 		#---------server channel ---begin

	)
