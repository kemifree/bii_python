# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 14:08:22 2017
淘宝关键词查询
@author: Acer
"""

import pandas as pd
#import MySQLdb
import time
from selenium import webdriver

def login_taobao_pv(username,password):
    
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
    
    ##浏览器最大化
    temp_login_info='登陆成功'
    
    return(temp_login_info,driver)

username=u'波奇网旗舰店:zjq'

password=u'a123456'
   
login_info,driver = login_taobao_pv(username,password)

#关键词 url解析
url  ='https://sycm.taobao.com/bda/toolbox/keyword/keyword_assistant.htm?spm=a21ag.7622621.0.0.Wrdo8D#/?device=2&page=searchKeyword'
driver.get(url)

##获取页面所有关键词元素
elements = driver.find_elements_by_css_selector('div.content.clearfix > ul.list>li')
##获取单个元素
for ele in elements:
    ele.find_element_by_css_selector('p.keyword > a').text


## 循环页面

keyword = []
url  ='https://sycm.taobao.com/bda/toolbox/keyword/keyword_assistant.htm?spm=a21ag.7622621.0.0.Wrdo8D#/?device=2&page=searchKeyword'
driver.get(url)
for i in range(30): 
    #默认进入关键词首页首页
    ##获取页面所有关键词元素
    elements = driver.find_elements_by_css_selector('div.content.clearfix > ul.list>li')
    ##获取单个元素
    for ele in elements:
        word = ele.find_element_by_css_selector('p.keyword > a').text
        print(word)
        keyword.append(word)
        ##循环点击下一页
    try:
        driver.find_element_by_css_selector('article#main a.ui-pagination-next').click()
    except:
        pass

import pandas as pd
db_key = pd.DataFrame(keyword,columns=['keyword'])
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/temp_etl?charset=utf8")
db_key.to_sql('app_keyword_dict',con=engine,if_exists='replace',index=False,chunksize=10000)


##pc

keyword = []
url  ='https://sycm.taobao.com/bda/toolbox/keyword/keyword_assistant.htm?spm=a21ag.7622621.0.0.Wrdo8D#/?device=1&page=searchKeyword'
driver.get(url)
for i in range(33): 
    #默认进入关键词首页首页
    ##获取页面所有关键词元素
    elements = driver.find_elements_by_css_selector('div.content.clearfix > ul.list>li')
    ##获取单个元素
    for ele in elements:
        word = ele.find_element_by_css_selector('p.keyword > a').text
        print(word)
        keyword.append(word)
        ##循环点击下一页
    try:
        driver.find_element_by_css_selector('article#main a.ui-pagination-next').click()
    except:
        pass

import pandas as pd
db_key = pd.DataFrame(keyword,columns=['keyword'])
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/temp_etl?charset=utf8")
db_key.to_sql('pc_keyword_dict',con=engine,if_exists='replace',index=False,chunksize=10000)

##店内关键词
keyword = []
url  ='https://sycm.taobao.com/bda/toolbox/keyword/keyword_assistant.htm?spm=a21ag.7622621.0.0.Wrdo8D#/?device=1&page=searchKeyword'
driver.get(url)
for i in range(21): 
    #默认进入关键词首页首页
    ##获取页面所有关键词元素
    elements = driver.find_elements_by_css_selector('div.content.clearfix > ul.list>li')
    ##获取单个元素
    for ele in elements:
        word = ele.find_element_by_css_selector('p.keyword > a').text
        print(word)
        keyword.append(word)
        ##循环点击下一页
    try:
        driver.find_element_by_css_selector('article#main div:nth-child(2) > div.content.clearfix > div > a.ui-pagination-next').click()
    except:
        pass

import pandas as pd
db_key = pd.DataFrame(keyword,columns=['keyword'])
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/temp_etl?charset=utf8")
db_key.to_sql('shop_keyword_dict',con=engine,if_exists='replace',index=False,chunksize=10000)

##行业热词榜
keyword = []
url = 'https://sycm.taobao.com/mq/words/industry_words.htm?spm=a21ag.7782695.LeftMenu.d374.Mb5BVw#/?cateId=29&dateRange=2017-04-13%7C2017-04-19&dateType=recent7&device=0'
driver.get(url)
for i in range(52):
    elements = driver.find_elements_by_css_selector('#main > div > div:nth-child(4) > div:nth-child(1) > div:nth-child(3) > div > div > table > tbody > tr')
    for ele in elements:
        word = ele.find_element_by_css_selector('td.text.keyword-row > a').text
        print(word)
        keyword.append(word)
    try:
        driver.find_element_by_css_selector('article#main div:nth-child(6) > div:nth-child(1) > div:nth-child(3) > div > div > div.ui-pagination.word-rank-pagination > a.ui-pagination-next > span').click()
    except:
        print('---ok')
import pandas as pd
db_key = pd.DataFrame(keyword,columns=['keyword'])
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/temp_etl?charset=utf8")
db_key.to_sql('hotsearch_keyword_dict',con=engine,if_exists='replace',index=False,chunksize=10000)


