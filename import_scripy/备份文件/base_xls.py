# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 16:37:36 2017
基础的文件夹删除，文件读取，文件写入数据库
@author: Acer
"""

import os
import pandas as pd
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
###############################################
###############################################
###########删除xls文件

class Base_xls(object):
    def delete_xlsfile(self,path):
        for root,dirs,files in os.walk(path):##文件夹的路径
            if files:   ##判断是否有文件
                for file_name in files:  ##循环文件的名称
                    if '.xls' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                        path = os.path.join(root,file_name)
                        print(path)
                        os.remove(path)
            temp_delete_info=u'xls文件清空完毕'
            return(temp_delete_info)
                
    #path='C:\\downloads'        
    #delete_info = delete_xlsfile(path)
    
    ###############################################
    ###############################################
    ###########读取文件
    def read_xlsfile(self,path,sheetname,business_name):
        for root,dirs,files in os.walk(path):##文件夹的路径
            if files:   ##判断是否有文件
                for file_name in files:  ##循环文件的名称
                    if '.xls' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                        path = os.path.join(root,file_name)
                        data = pd.ExcelFile(path)
                        table_sheet = data.parse(sheetname=sheetname,skiprows=3)
                        table_sheet['店铺']=business_name
                        temp_read_info='xls文件读取成功'
                        return(temp_read_info,table_sheet)
                            
    
    #path='C:\\downloads'
    
    #info_read,sheet=read_xlsfile(path=path,business_name='波奇网旗舰店')
    
    
    ###############################################
    ###############################################
    ###写入到数据库
    def to_mysql(self,local_table,server_table):
        try:
            
            conn = MySQLdb.connect(host='172.16.57.72', charset='utf8',port=3306,user='step', passwd='123456', db='tmall')   
            local_table.to_sql(name=server_table,con=conn,flavor='mysql',if_exists='append',index=False,chunksize=10000) 
            temp_sql_info='数据库写入成功'
        except:
            temp_sql_info='数据库写入失败'
        return(temp_sql_info)
    
    #local=sheet
    #sever_table_name='temp'
    #info_sql = to_mysql(local_table=local,server_table= sever_table_name)


#xls = Base_xls()
#path='C:\\downloads'        
#delete_info = xls.delete_xlsfile(path)