# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:33:34 2017

@author: Acer
"""
import re
import pandas as pd
import requests
import time
from selenium import webdriver
from sqlalchemy import create_engine
import time
from datetime import datetime, timedelta
import urllib.parse as urlparse
from urllib.parse import urlencode



def login_taobao(username,password):
    
    ##下载路径位置和谷歌selenium驱动器位置
    options = webdriver.ChromeOptions()
    
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\Acer\\Downloads'}
    
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
    cookie_list = driver.get_cookies()
    ##浏览器最大化
    driver.maximize_window()
    
    #temp_login_info='登陆成功'
    
    return(cookie_list,driver)

    
#----


def ger_data(date_range=1):
    yesterday = (datetime.date(datetime.now()) - timedelta(days=1)).strftime('%Y-%m-%d')
    source = {
    'sourceDataType':0,
    'dateRange':yesterday+'|'+yesterday, #默认选择昨天
    'dateType':'day',
    'device':1,#默认商品类目
    'orderDirection':'true',
    'orderField':'cateUv',
    'type':1
    }
    date_range = date_range
    for day in range(date_range):
        date_value = datetime.date(datetime.now()) -timedelta(days=1) - timedelta(days=day) #默认取昨天的数据
        date_value = date_value.strftime('%Y-%m-%d')
        dateRange = {'dateRange':date_value+'|'+date_value} 
        source.update(dateRange)
        ##url地址解析
        try:
            url_base = 'https://sycm.taobao.com/bda/items/classifyanaly/getClassifyDetail.json?'
            response = session.get(url_base,headers = headers,params=source) 
            content = response.json()
            data_values = content['data']['list']
            print('url解析成功')
        except:
            print('url解析失败，跳出本次循环，执行下一次循环')
            continue
        ##数据解析
        try:
            df = get_content(data_values)
            df['店铺'] = shopname
            print('content内容解析成功')
        except:
            print('content内容解析失败,跳出本次循环，执行下一次循环')
            continue
        ##存入数据库
        ##写入数据库
        try:
            server_name = '商品分类'
            engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
            df.to_sql(server_name,con=engine,if_exists='append',index=False,chunksize=10000)
            print('数据写入完成')
        except:
            print('数据写入失败')

def get_content(data_values):
    df_names = {
    'addCartItemCnt':'加购件数',
    'cateId':'类型编号',
    'cateItemCnt':'商品数',
    'cateName':'商品类别',
    'cateUv':'访客数',
    'orderRate':'下单转化率',
    'parentCateId':'父类别编号',
    'father':'父类别名称',
    'children':'子类别名称',
    'class':'类别'
    }
    df = pd.DataFrame([],columns = ['father','addCartItemCnt', 'cateId', 'cateItemCnt', 'cateName', 'cateUv',
           'children', 'orderRate', 'parentCateId'])
    for i in range(len(data_values)):
        #data_values[i]['children']
        father = data_values[i]['cateName']
        children = data_values[i]['children']
        df_father = pd.DataFrame([data_values[i]])
        df_father['father'] = data_values[i]['cateName']
        df_father['class'] = '父类别'
        if len(children) > 0:
            data_values[i]['children']
            df_children = pd.DataFrame(data_values[i]['children'])
            df_children['father'] = data_values[i]['cateName']
            df_father['class'] = '子类别'
        df = pd.concat([df,df_father,df_children])
    df['children'] = None
    df.ix[df['father'] == df['cateName'],'class'] = '父类别'
    df.ix[df['father'] != df['cateName'],'class'] = '子类别'
    df =df.rename(columns = df_names)
    return(df)

if __name__ == "__main__": 
    username=u'波奇网旗舰店:zjq'
    password=u'a123456'
    shopname = '波奇网旗舰店'
    cookies,driver = login_taobao(username,password)
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    headers={
    "accept":"*/*",
    "accept-encoding":"gzip, deflate, sdch, br",
    "accept-language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2",
    "referer":"https://sycm.taobao.com/mq/industry/overview/overview.htm?spm=a21ag.7782695.LeftMenu.d293.aaaYIy",
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    
    #异常商品 -流量下跌
    ger_data(date_range=1)