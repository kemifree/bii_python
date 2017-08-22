# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 11:03:36 2017

@author: Acer
"""

import os,sys
import time
python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy'
sys.path.append(python_path)
from base_xls import Base_xls
from taobao_selenium import Taobao

xls  = Base_xls() 
taobao = Taobao()

def reports_local_mysql(path,username,password,
                          url,title_name,
                          sheename,business_name,
                          sever_table_name
                          ):
                              
    delete_info = xls.delete_xlsfile(path)
    login_info,driver = taobao.login_taobao(username,password)
    info_taobao_xls = taobao.downloads_taobao_xls(driver=driver,url=url,title_name=title_name )
    time.sleep(5)
    info_read,sheet=xls.read_xlsfile(path=path,sheetname = sheename ,business_name=business_name)
    info_quit_temp = taobao.quit_driver(driver)
    info_sql = xls.to_mysql(local_table=sheet,server_table= sever_table_name)
    
    #return(delete_info,login_info,info_taobao_xls,info_read,info_sql)
    return(info_read,info_sql)
    
##文件下载存放地址    
path='C:\\Users\\Acer\\Downloads'  
username=u'波奇网旗舰店:zjq'
password=u'a123456' 

##我的报表url及报表名称
url='https://sycm.taobao.com/adm/user_report.htm?spm=a21ag.7622622.LeftMenu.d442.MdL2C7'
title_name = '日运营明细表'

##下载表格名称，及店铺
sheetname ='自助取数'
business_name='波奇网旗舰店'

##存入数据库表的名称
sever_table_name='波奇网旗舰店'

info_read,info_sql = reports_local_mysql(path,username,password,url,title_name,sheetname,
                                         business_name,sever_table_name)    