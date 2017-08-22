# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:10:13 2016

@author: Acer
"""

# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json ,requests,os,uniout
import random
import _uniout
import pandas as pd
from pandas import DataFrame
import xlrd,openpyxl

##读取文件
import pandas as pd

##读取excel文档地址信息
def xlsx_read(path=path,sheet_name=u'Sheet1'):
    xlsx = pd.ExcelFile(path)
    sheet = xlsx.parse(sheet_name)
    return(sheet)
#sheet = xlsx_read()
##选取excel文档的需要地址信息
def sheet_values(sheet=sheet,address=u'地址'):
    sheet.columns=sheet.columns.str.strip()
    sheet.columns
    #sheet[u'地址']=sheet[u'收货地址'].str.replace(" ","")
    sheet[address]=sheet[u'收货地址'].str.replace(" ","")
    del sheet[u'收货地址']
    #del sheet[u'收货人姓名.1']
    location_data = sheet[[u'地址',u'收货人姓名']]
    return(location_data)
#location_data =  sheet_values(sheet)


##地址转换成url地址
def url_add(location):
    import random 
    AK = random.sample(api_key, 1)
    key = ",".join(AK)
    url = 'http://restapi.amap.com/v3/geocode/geo?key=' + key + '&address=' + location
    return(url)
#location_data['url']=location_data[u'地址'].apply(url_add)

##调用API，返回信息，'URLError: <urlopen error timed out> All times is failed ' 再次调用2次
def requests_get(url,n=2):
    import requests
    global Max_Num
    Max_Num = n
    for i in range(Max_Num):
        try:
            return(requests.get(url))
        except:
             if i < Max_Num - 1:
                 continue
             else:
                 pass

##results=pool.map(requests_get,sheet['url'])
##多线程调用
def ThreadPool(list_url,n=4):
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(n)
    results=pool.map(requests_get,list_url)
    return results
#函数实例化
#results=ThreadPool(location_data['url'])

def url_data(results):
    import json
    import pandas as pd
    n_ok=0
    n_false=0
    location_items = ['formatted_address','location','province','city','district','street','number','lng','lat']
    temp = pd.DataFrame([],columns=location_items)
    for resq in results:
        try:
            data=json.loads(resq.text)
            n_ok=n_ok+1
            print str(n_ok)+'正在解析ing...................'
            '''
            上面有这里就只是显示下
            location_items = ['formatted_address','location','province','city','district','street','number']
            '''
            location_data = pd.DataFrame(data[u'geocodes'],columns=location_items)
            location_data['lng'] = location_data['location'][0].split(',')[0]  ##经度
            location_data['lat'] = location_data['location'][0].split(',')[1]  ##维度
            temp = pd.concat([temp,location_data])
            location_address_data = temp

        except:
            n_false=n_false+1
            print str(n_false)+'解析错误'
            pass
    return(location_address_data)
##测试用例
#data = url_data(results)


api_key=['8191d1b4718e17d8b5b2e2b9a9f31bb0','09b7d72a3dc2bd30e86b23dc11b382fc','efe64265959124ade43857e06322577b','00210b231b1895ddfc190142ccbfda59']


path = 'C:\\Users\\Acer\\Desktop\\temp_location_1123.xlsx'
path = 'C:\\Users\\Acer\\Desktop\\orders_location_1111.xlsx'
path = unicode(path,encoding='utf-8')


sheet = xlsx_read(path=path,sheet_name=u'Sheet1')
location_data =  sheet_values(sheet=sheet,address=u'地址')
location_data['url']=location_data[u'地址'].apply(url_add)
results=ThreadPool(location_data['url'])
data_values = url_data(results)
data_values.head()
sheet
help(sheet.to_excel)