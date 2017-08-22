# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 17:41:51 2017

@author: Acer
"""

import os,sys
import time
path = 'C:\\Users\\Acer\\Desktop\\import_scripy'
sys.path.append(path)
from base_xls import Base_xls

from taobao_selenium import Taobao



xls  = Base_xls() 

taobao = Taobao()
####################################################
####################################################
##########登陆网站
username=u'波奇网旗舰店:zjq'
password=u'a123456'
login_info,driver = taobao.login_taobao(username,password)

####################################################
####################################################
##########清空xls数据

path='C:\\Users\\Acer\\Downloads'        
delete_info = xls.delete_xlsfile(path)

####################################################
####################################################
##########下载数据
driver=driver
url='https://sycm.taobao.com/adm/user_report.htm?spm=a21ag.7622622.LeftMenu.d442.MdL2C7'
title_name = '日运营明细表'
info_taobao_xls = taobao.downloads_taobao_xls(driver=driver,url=url,title_name=title_name )

driver = driver

info_quit_temp = taobao.quit_driver(driver)

####################################################
####################################################
##########读取数据
time.sleep(5)
path='C:\\Users\\Acer\\Downloads' 
sheename ='自助取数'
business_name='波奇网旗舰店'
info_read,sheet=xls.read_xlsfile(path=path,sheetname = sheename ,business_name=business_name)

####################################################
####################################################
##########写入数据库
local=sheet
sever_table_name='temp0105'
info_sql = xls.to_mysql(local_table=local,server_table= sever_table_name)
