#!/usr/bin/python
#-*- coding: UTF-8 -*- 

import sys
import json
import string

#coding:utf-8

# appkey
appKey = "2064302565"
secret = "BB9318B102E320C09B8AB9D5229B5668DB1C00D0"

#调试环境
# environment = "jzs"
#environment = "debug"
environment = "production"

api_server_list = {
	"jzs":"192.168.11.73",
	"debug":"192.168.1.207",
	"production":"api.daoke.me",  #正式环境
}

ENVI_SERVER_LIST = (
	("jzs","jzs localhost"),
	("debug","线下调试"),
	("production","正式环境"),
)

api_post_list = {
	"jzs":80,
	"debug":80,
	"production":80,
}

api_remark_list = {
	"jzs":"jzs localhost",
	"debug":"线下调试",
	"production":"正式环境",
}
