# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 18:16:58 2017
##下载流量来源
@author: Acer
"""
'''
import time
import sys
python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy'
sys.path.append(python_path)
from base_file import Base_file
base  = Base_file() 

username=u'波奇网旗舰店:zjq'
password=u'a123456'
login_info,driver = base.login_taobao_pv(username,password)

path_downloads = 'C:\\Users\\Acer\\Downloads'
info  = base.delete_xlsfile(path=path_downloads)

path='C:\\Users\\Acer\\Downloads'
#sheetname = 'PC流量来源'
sheetname = u'无线流量来源'
business_name='波奇网旗舰店'
info_read,sheet=base.read_pv(path=path,sheetname=sheetname,business_name=business_name)

local=sheet
sever_table_name='temp_10'
info_sql = base.to_mysql(local_table=local,server_table= sever_table_name)
'''

####################################################



def downloads_pv(path,sheetname,business_name,sever_table_name,url,driver):
    
    
    driver.get(url)
    ##今日实时
    driver.find_element_by_css_selector('div.ebase-DatePicker__main > span.ebase-DatePicker__mainText').click()
    ##自然日
    driver.find_element_by_css_selector('div#app li:nth-child(5) > span.ebase-DatePicker__rangeText').click()
    ##获取日期table
    data_table=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/table')
    ##获取本月所有日期
    rows=data_table.find_elements_by_css_selector('tr.oui-calendar-date-column > td.current-month')
    ##获取本月不能显示日期
    disabled_rows=data_table.find_elements_by_css_selector('tr.oui-calendar-date-column > td.current-month.disabled-element')
    ###缓冲机制---点击pc，无线端按钮
    driver.find_element_by_css_selector('a.common-filter-select.oui-select-trigger.oui-popup-trigger >span.oui-select-label').click()
    driver.implicitly_wait(30)
    ###循环下载表格
    for i in range(len(rows)-len(disabled_rows)):
        driver.find_element_by_css_selector('div.ebase-DatePicker__main > span.ebase-DatePicker__mainText').click()
        
        driver.find_element_by_css_selector('div#app li:nth-child(5) > span.ebase-DatePicker__rangeText').click() 
        
        rows[i].get_attribute("data-value")
        rows[i].click()
        ##点击pc，无线端按钮
        driver.find_element_by_css_selector('a.common-filter-select.oui-select-trigger.oui-popup-trigger >span.oui-select-label').click()
        ##################################################################################################
        ###########################选择PC端#######################################################
        ##################################################################################################
        ##选择PC端
        driver.find_element_by_css_selector('div.oui-scroller > ul.oui-select-menu.oui-scroll-noBar.oui-scroller-content  >  li:nth-child(1)').click()
        #缓存机制，否则下载按钮看不到
        driver.find_element_by_css_selector('div#app span > span.num').click()
        #time.sleep(3)

        
        ###########数据预处理
        try:
            
            ##删除存在的文件
            info  = base.delete_xlsfile(path=path)
            
            ##下载文件
            driver.find_element_by_css_selector('div#card-shop-source-01 a > i').click()
            
            time.sleep(3)
            
            sheetname = u'PC流量来源'
            
            info_read,sheet=base.read_pv(path=path,sheetname=sheetname,business_name=business_name,skiprows=5)
            
            sever_table_name = u'PC流量来源'            
                        
            info_sql = base.to_mysql(local_table=sheet,server_table= sever_table_name)
            
            info_pc = u'数据预处理成功'
        except:
            info_pc = u'数据预处理失败'
                
        ##无线端
        ##################################################################################################
        ###########################选择PC端#######################################################
        ##################################################################################################
        ##点击pc，无线端按钮
        driver.find_element_by_css_selector('a.common-filter-select.oui-select-trigger.oui-popup-trigger >span.oui-select-label').click()
        ##选择无线端
        driver.find_element_by_css_selector('div.oui-scroller > ul.oui-select-menu.oui-scroll-noBar.oui-scroller-content  >  li:nth-child(2)').click()
        #缓存机制，否则下载按钮看不到
        driver.find_element_by_css_selector('div#app span > span.num').click()
        #time.sleep(3)
        ##下载
        driver.find_element_by_css_selector('div#card-shop-source-01 a > i').click()
        
                ###########数据预处理
        try:
            ##删除存在的文件
            info  = base.delete_xlsfile(path=path)
            
            ##下载
            driver.find_element_by_css_selector('div#card-shop-source-01 a > i').click()
            
            time.sleep(3)
            sheetname = u'无线流量来源'
            
            info_read,sheet=base.read_pv(path=path,sheetname=sheetname,business_name=business_name,skiprows=5)
            
            sever_table_name = u'无线流量来源'
            
            info_sql = base.to_mysql(local_table=sheet,server_table= sever_table_name)
            
            info_wlan = u'数据预处理成功'
        except:
            info_wlan = u'数据预处理失败'
    return(info_pc,info_wlan)

############################################################

import sys,time
from selenium.webdriver.common.keys import Keys
python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy'
sys.path.append(python_path)
from base_file import Base_file
base  = Base_file() 


username=u'波奇网旗舰店:zjq'
password=u'a123456'
login_info,driver = base.login_taobao_pv(username,password)


url = 'https://sycm.taobao.com/flow/monitor/shopsource?activeKey=1&dateRange=2017-01-09%7C2017-01-09&dateType=today&device=1&spm=a21ag.8198214.LeftMenu.d754.RhXcQi'
path='C:\\Users\\Acer\\Downloads'
sheetname_temp = u'流量来源'
business_name='波奇网旗舰店'
sever_table_name_temp ='流量来源'
pc,wlan = downloads_pv(path=path,sheetname=sheetname_temp,
                       business_name=business_name,sever_table_name=sever_table_name_temp,
                       url=url,driver=driver)
            
        
'''        
##热销店铺帮

import pandas as pd

business_rank_columns = ['date','rank','business_name','seller_index']

business_rank = pd.DataFrame(columns=business_rank_columns)

url = 'https://sycm.taobao.com/mq/industry/rank/industry.htm?spm=a21ag.7749217.LeftMenu.d343.aFTowP#/?cateId=29&categoryId=29&dateRange=2017-01-09%7C2017-01-09&dateRangePre=2017-01-09%7C2017-01-09&dateType=recent1&dateTypePre=recent1&device=0&devicePre=0&itemDetailType=1&rankTabIndex=2&seller=-1&view=rank'

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
previous_rows=data_table.find_elements_by_css_selector('tr.ui-calendar-date-column > td.previous-month')


##缓冲机制--点击搜索

driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/a').click()

len(current_rows)

len(disabled_rows)

len(previous_rows)

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

    element.send_keys(u"波奇网旗舰店")
    ##搜索
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/a').click()
    ##获取搜索店铺名称
    temp_business_name =driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div/div/div[3]/div/div/table/tbody/tr/td[2]/a/div/span/span[2]').text

    ##条件判断
    if temp_business_name == u"波奇网旗舰店":
        rank = driver.find_element_by_css_selector('table.table-ng.table-ng-basic > tbody > tr > td.raw').text
        business_name = driver.find_element_by_css_selector('table > tbody > tr > td:nth-child(2) > a > div > span > span.highlight').text
        num = driver.find_element_by_css_selector('table.table-ng.table-ng-basic > tbody > tr >td:nth-child(4)').text
        
        date = current_rows[i].get_attribute("data-value")    
        
        temp_business_rank = pd.DataFrame([[date,rank,business_name,num]],columns=business_rank_columns)        
        
        business_rank = pd.concat([business_rank,temp_business_rank])
        
'''   
    
    

    