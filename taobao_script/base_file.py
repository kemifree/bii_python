# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 18:08:58 2017

@author: Acer
"""
import os,re
import shutil
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sqlalchemy import create_engine
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
#################删除xls文件

class Base_file(object):
    def delete_xlsfile(self,path):
        for root,dirs,files in os.walk(path):##文件夹的路径
            if files:   ##判断是否有文件
                for file_name in files:  ##循环文件的名称
                    if '.xls' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                        xls_path = os.path.join(root,file_name)
                        #print(xls_path)
                        taobao_directory = 'C:\\taobao_downloads' ##把文件copy到哪里？
                        if os.path.exists(taobao_directory):
                            
                            shutil.copy(xls_path,taobao_directory)
                            
                        else :
                            os.mkdir(taobao_directory)
                        
                        os.remove(xls_path)
            temp_delete_info=u'xls文件清空完毕'
            return(temp_delete_info)
    #path_downloads = 'C:\\Users\\Acer\\Downloads'
    #info  = delete_xlsfile(path=path_downloads)
    #########################判断xls文件是否下载成功
    ##读取浏览来源数据####################################################################   
    def xls_crdownload(self,path):
        for root,dirs,files in os.walk(path):##文件夹的路径
            if files:   ##判断是否有文件
                for file_name in files:  ##循环文件的名称            
                    if '.xls.crdownload' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                        #xls_path = os.path.join(root,file_name)
                        print('chrome正在缓冲下载ing,请等待下载完毕')
                        time.sleep(15)
                    xls_crdownload_info = u'下载超时'
            return(xls_crdownload_info)

    #import os
    #import time 
    #path = 'C:\\Users\\Acer\\Downloads'
    #info  = xls_crdownload(path)    
    #########################读取文件
    ##读取浏览来源数据####################################################################
    def read_table(self,path,sheetname,skiprows):
        temp_read_info =None
        table_sheet = None
        for root,dirs,files in os.walk(path):##文件夹的路径
            if files:   ##判断是否有文件
                for file_name in files:  ##循环文件的名称
                    #if '.xls' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                    if 'xls.crdownload' in file_name:
                        time.sleep(15)
                    elif file_name.endswith('xls'): ##判断以xlsx结尾的文件是否在文件名称的末尾
                    #elif '.xls' in file_name:
                        path = os.path.join(root,file_name)
                        print('文件下载成功临时存放地址--'+path+'正在向数据库写入ing')
                        data = pd.ExcelFile(path)
                        table_sheet = data.parse(sheetname=sheetname,skiprows=skiprows)
                        ##判断表中是否有日期
                        date =u'日期'
                        if  date in table_sheet.columns:
                            table_sheet['date_temp'] = table_sheet[date]
                            del table_sheet[date]
                            table_sheet['日期'] = re.search(r'\d{4}-\d{2}-\d{2}.*\d{4}-\d{2}-\d{2}',path).group(0)
                            #table_sheet['min_pathdate'] = re.findall(r'\d{4}-\d{2}-\d{2}',path)[0]
                            #table_sheet['max_pathdate'] = re.findall(r'\d{4}-\d{2}-\d{2}',path)[1]
                        else :
                            table_sheet['日期'] =  re.search(r'\d{4}-\d{2}-\d{2}.*\d{4}-\d{2}-\d{2}',path).group(0)
                            #table_sheet['min_pathdate'] = re.findall(r'\d{4}-\d{2}-\d{2}',path)[0]
                            #table_sheet['max_pathdate'] = re.findall(r'\d{4}-\d{2}-\d{2}',path)[1]
                        temp_read_info='xls文件读取成功'
                        return(temp_read_info,table_sheet)
                            
    
    #path='C:\\Users\\Acer\\Downloads'
    #sheetname = 'PC流量来源'
    #sheetname = u'无线流量来源'
    #business_name='波奇网旗舰店'
    #info_read,sheet=read_xlsfile(path=path,sheetname=sheetname,business_name=business_name)
    
    def to_mysql(self,local_table,server_table):
        try: 
            engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")            
            local_table.to_sql(name=server_table,con=engine,if_exists='append',index=False,chunksize=10000)
            temp_sql_info='数据库写入成功'
            engine.drop
            print(temp_sql_info)
        except:
            temp_sql_info='数据库写入失败'
            print(temp_sql_info)
        return(temp_sql_info)
    
    #local=sheet
    #sever_table_name='temp_10'
    #info_sql = to_mysql(local_table=local,server_table= sever_table_name)
    
    
    def login_taobao(self,username,password):
        
        ##下载路径位置和谷歌selenium驱动器位置
        options = webdriver.ChromeOptions()
        
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\downloads_taobao'}
        
        options.add_experimental_option('prefs', prefs)

        
        driver = webdriver.Chrome("C:\\Users\\Acer\\Desktop\\git\\selenium\\chromedriver_win32\\chromedriver.exe",chrome_options=options)
        
        driver.get('https://sycm.taobao.com/custom/login.htm')
        
        
        frame = driver.find_element_by_xpath('//*[@id="app"]/div/section[1]/div/div[1]/iframe')
        
        driver.switch_to.frame(frame)
        
        
        driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys(username)
        
    
        driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(password)
    
        ##
        driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').submit()
        time.sleep(5)
        #print (driver.page_source)
        
        driver.implicitly_wait(30)
        
        ##直接定位到主页
        driver.get('https://sycm.taobao.com/portal/index.htm?spm=a21ag.8106233.logo.1.kxzbwq')
        
        ##浏览器最大化
        driver.maximize_window()
        
        temp_login_info='登陆成功'
        
        return(temp_login_info,driver)
    
    #username=u'波奇网旗舰店:zjq'
    
    #password=u'a123456'
       
    #login_info,driver = login_taobao(username,password)


