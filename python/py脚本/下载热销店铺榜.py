# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:36:49 2017
##下载热销店铺帮
@author: Acer
"""

def business_rank(url,driver,business_name):
    
    business_rank_columns = ['date','rank','business_name','seller_index']

    business_rank = pd.DataFrame(columns=business_rank_columns)
    
    driver.get(url)
    ##日期按钮框
    driver.find_element_by_css_selector('div.dtpicker.common-filter-dtpicker > div.dtpicker-main > i.icon-cal').click()
    ##选取日
    
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div/div[1]/div[2]/ul/li[3]/span[1]').click()
    
    ##选取日期框table
    data_table =driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div/div[2]/table[1]')
    ##选取本月日期
    current_rows=data_table.find_elements_by_css_selector('tr.ui-calendar-date-column > td.current-month')
    ##选取不可见日期
    disabled_rows=data_table.find_elements_by_css_selector('tr.ui-calendar-date-column > td.current-month.disabled-element')
    ##选取本月含上月日期
    #previous_rows=data_table.find_elements_by_css_selector('tr.ui-calendar-date-column > td.previous-month')
    ##缓冲机制--点击搜索   
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/a').click()    
    for i in range(len(current_rows)-len(disabled_rows)):
        ##日期按钮框
        driver.find_element_by_css_selector('div.dtpicker.common-filter-dtpicker > div.dtpicker-main > i.icon-cal').click()
        ##选取日
    
        driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div/div[1]/div[2]/ul/li[3]/span[1]').click()
        ##循环
        current_rows[i].get_attribute("data-value")
        current_rows[i].click()
        
        ##搜索
        driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/input').clear()
        ##填写
        element = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/input')
        
        element.clear()
    
        element.send_keys(business_name)
        ##搜索
        driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/a').click()
        ##获取搜索店铺名称
        temp_business_name =driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/table/tbody/tr/td[2]/a/div/span/span[2]').text
    
        ##条件判断
        if temp_business_name == business_name:
            rank = driver.find_element_by_css_selector('table.table-ng.table-ng-basic > tbody > tr > td.raw').text
            business_name = driver.find_element_by_css_selector('table > tbody > tr > td:nth-child(2) > a > div > span > span.highlight').text
            num = driver.find_element_by_css_selector('table.table-ng.table-ng-basic > tbody > tr >td:nth-child(4)').text
            
            date = current_rows[i].get_attribute("data-value")    
            
            temp_business_rank = pd.DataFrame([[date,rank,business_name,num]],columns=business_rank_columns)        
            
            business_rank = pd.concat([business_rank,temp_business_rank])  
            
    return(business_rank)


import sys,time
from selenium.webdriver.common.keys import Keys
python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy'
sys.path.append(python_path)
from base_file import Base_file
base  = Base_file() 

username=u'********'
password=u'a123456'
login_info,driver = base.login_taobao_pv(username,password)



import pandas as pd
url = 'https://sycm.taobao.com/mq/industry/rank/industry.htm?spm=a21ag.7749217.LeftMenu.d343.aFTowP#/?cateId=29&categoryId=29&dateRange=2017-01-09%7C2017-01-09&dateRangePre=2017-01-09%7C2017-01-09&dateType=recent1&dateTypePre=recent1&device=0&devicePre=0&itemDetailType=1&rankTabIndex=2&seller=-1&view=rank'
driver =driver
business_name = u"波奇网旗舰店"


business_rank_sheet = business_rank(url,driver,business_name)