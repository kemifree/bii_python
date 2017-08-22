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
from datetime import datetime
from sqlalchemy import create_engine

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
 
##选着switch 

def get_switch(driver):
    #选择流量下跌
    switch_menu = driver.find_element_by_css_selector('ul.ui-switch-menu')
    switch_li = switch_menu.find_elements_by_css_selector('li')    
    table_name ={
    'title' : '商品名称',
    'href' : 'url链接',
    'product_id' : '商品ID',
    'datetime' : '发布时间',
    'date' : '日期'
    }    
    for child in range(len(switch_li)):
        try:
            switch_li[child].find_element_by_css_selector('a').click()
        except:
            print('异常商品切换错误,跳过本次循环执行下一次循环')
            continue
            
        time.sleep(1)
        print('异常商品类型----'+switch_li[child].find_element_by_css_selector('a').text)
        try:
            df = get_content(driver=driver)
            print('数据采集成功')
        except:
            print('数据采集失败，跳过本次循环，执行下一次循环')
            continue
            
        if child == 0:
            table_name.update({'col_2_num' : '上个周期7天浏览量'})
            table_name.update({'col_3_num' : '最近7天浏览量'})
            df = df.rename(columns = table_name)
            df['采集日期'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')
            df['异常类型'] = switch_li[child].find_element_by_css_selector('a').text
        elif child == 1:
            table_name.update({'col_2_num' : '最近7天访客数'})
            table_name.update({'col_3_num' : '最近7天日均支付转化率'})
            df = df.rename(columns = table_name)
            df['采集日期'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')
            df['异常类型'] = switch_li[child].find_element_by_css_selector('a').text
        elif child == 2:
            table_name.update({'col_2_num' : '最近7天浏览量'})
            table_name.update({'col_3_num' : '最近7天日均跳出率'})
            df = df.rename(columns = table_name)
            df['采集日期'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')
            df['异常类型'] = switch_li[child].find_element_by_css_selector('a').text
        elif child == 3:
            table_name.update({'col_2_num' : '上周期7天支付金额'})
            table_name.update({'col_3_num' : '最近7天支付金额'})
            df = df.rename(columns = table_name)
            df['采集日期'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')
            df['异常类型'] = switch_li[child].find_element_by_css_selector('a').text
        elif child == 4:
            table_name.update({'col_2_num' : '上个周期7天访客数'})
            table_name.update({'col_3_num' : '上个周期7天支付金额'})
            df = df.rename(columns = table_name)
            df['采集日期'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')
            df['异常类型'] = switch_li[child].find_element_by_css_selector('a').text
        elif child == 5:
            table_name.update({'col_2_num' : '最近7天加购件数'})
            table_name.update({'col_3_num' : '最近1天加购件数'})
            df = df.rename(columns = table_name)
            df['采集日期'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')
            df['异常类型'] = switch_li[child].find_element_by_css_selector('a').text
        else:
            pass        
        ##写入数据库
        try:
            server_name = '异常商品'
            engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
            df.to_sql(server_name,con=engine,if_exists='append',index=False,chunksize=10000)
            print('数据写入完成')
        except:
            print('数据写入失败')


##选择具体数据

def get_content(driver):
    content = driver.find_element_by_css_selector('div.content')
    #选取页面
    page_total = content.find_element_by_css_selector('div.ui-pagination.pull-right span.ui-pagination-total').text
    page_number = re.findall(r'\d+',page_total)[0]
    #选择下一页
    content_list =[]
    df = pd.DataFrame(content_list)
    for i in range(int(page_number)):
        
        if i != 0: #当前页面不加载
            ##当前页面数据采集完毕，进入下一页
            content.find_element_by_css_selector('div.ui-pagination.pull-right a.ui-pagination-next').click()  
        #选取table,采集数据
        table = content.find_elements_by_css_selector('div.table-body div.row')
        for item in range(len(table)):
            content_dict = {}
            print('正在解析---' +table[item].find_element_by_css_selector('p.title > a').text)
            content_dict['title'] = table[item].find_element_by_css_selector('p.title > a').text
            content_dict['href'] = table[item].find_element_by_css_selector('p.title > a ').get_attribute('href')
            content_dict['product_id'] = re.findall(r'\d.*$',content_dict['href'])[0]
            content_dict['datetime'] = table[item].find_element_by_css_selector('p.datetime ').text
            content_dict['date'] = re.findall(r'\d{4}-\d{2}-\d{2}',content_dict['datetime'])[0]    
            content_dict['col_2_num'] =table[item].find_element_by_css_selector('div.row span.col.col-2.num').text    
            content_dict['col_3_num'] =table[item].find_element_by_css_selector('div.row span.col.col-3.num').text    
            content_dict['col_3_num'] = re.match(r'\d+',content_dict['col_3_num']).group(0)
            content_list.append(content_dict)  
            len(content_list)
    df = pd.DataFrame(content_list)
    print('数据采集成功')
    return df

   
if __name__ == "__main__": 
    username=u'波奇网旗舰店:zjq'
    password=u'a123456'
    cookies,driver = login_taobao(username,password)
    #异常商品 -流量下跌
    url = 'https://sycm.taobao.com/bda/items/itemanaly/item_exception.htm?'
    driver.get(url) 
    get_switch(driver)
    
    #此数据集重复采集，以避免中间出错；
    
    