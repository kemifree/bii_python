# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:39:22 2017
商品效果明细明细数据下载
@author: Acer
"""

import sys
import re
import time
from datetime import datetime, timedelta
import urllib.parse as urlparse
from urllib.parse import urlencode
from sqlalchemy import create_engine

python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy\\taobao_script'
sys.path.append(python_path)

from base_file import Base_file
base  = Base_file() 
username=u'波奇网旗舰店:zjq'
password=u'a123456'
login_info,driver = base.login_taobao(username,password)

path='C:\\downloads_taobao'
business_name='波奇网旗舰店'
source = '商品效果'


url_base = 'https://sycm.taobao.com/bda/download/excel/items/effect/ItemEffectExcel.do?'
yesterday = (datetime.date(datetime.now()) - timedelta(days=1)).strftime('%Y-%m-%d')
recent_7 = (datetime.date(datetime.now()) - timedelta(days=7)).strftime('%Y-%m-%d')

params = {
'dateRange':recent_7+'|'+yesterday, #默认选择昨天
'dateType':'recent7',
'device':0,#默认选择全部
'orderDirection':'false',
'orderField':'itemPv',
'type':'0'
}

def url_recent_7_download(driver=driver,path=path,url_base=url_base,params=params):
    #默认取前1天数据：    
    device_dict={0:'全部',1:'PC',2:'无线'}
    for key in  device_dict:
        device = key
        device_name = device_dict[key]
        device = {'device':device}
        print('正在下载最近7天----'+device_name+'-商品效果----请耐心等待')
        params.update(device)
        #下载数据，并存放到数据库中
        download(driver=driver,url_base=url_base,params=params,path=path)


def download(driver=driver,url_base=url_base,params=params,path=path):
    try:
        ##删除存在的文件
        info  = base.delete_xlsfile(path=path) 
        #------------------------------
        #-------下载数据---------
        #url_base = 'https://sycm.taobao.com/bda/download/excel/items/effect/ItemEffectExcel.do?'
        for i in range(5):
            try:
                url_download = url_base + urlencode(params)
                driver.get(url_download)
                time.sleep(3)
                break
            except:
                print('chrome文件url地址解析失败，下载失败,请检测失败原因')
        #检测文件是否下载完成
        base.xls_crdownload(path)
        #------------------------------
        #读取数据
        for i in range(5):
            try:
                info_read,sheet=base.read_table(path=path,sheetname=0,skiprows=3)
                break
            except:
                print('文件正在下载中ing-----正在等待----'+str(i)+'-----请稍等')
            
        sheet[u'店铺']=business_name
        datetype ='最近7天'
        sheet[u'日期类型']=datetype
        sheet[u'start日期'] = sheet['日期'].str.findall(r'\d{4}-\d{2}-\d{2}',flags = re.IGNORECASE).str.get(0)
        #sheet[platform] = platform #表中已经自带渠道
        sever_table_name =business_name+source+datetype                                 
        engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")  
        #          
        sheet.to_sql(name=sever_table_name,con=engine,if_exists='append',index=False,chunksize=10000)
        engine.drop  
        #info = u'数据预处理成功'
        print('第----------数据预处理成功')
    except:
        print('第----------数据预处理失败') 





if __name__ == "__main__":
    business_name = '波奇网旗舰店'
    datetype ='最近7天'
    source = '商品效果'
    sever_table_name =business_name+source+datetype 
    engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")  
    #删除表
    sql = 'drop table if exists  ' + sever_table_name
    engine.execute(sql)
    engine.drop
    #插入最近7天数据
    url_recent_7_download(driver=driver,path=path,url_base=url_base,params=params)
