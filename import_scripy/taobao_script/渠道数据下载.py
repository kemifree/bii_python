# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:27:27 2017
#淘宝流量数据下载
@author: Acer
"""

import sys,time
from datetime import datetime

python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy\\taobao_script'
sys.path.append(python_path)
from base_file import Base_file
base  = Base_file() 

username=u'波奇网旗舰店:zjq'
password=u'a123456'
login_info,driver = base.login_taobao(username,password)

path='C:\\downloads_taobao'
business_name='波奇网旗舰店'
source = '流量来源'


#------------------------------

#当月的数据

    #下载流量地图
url = 'https://sycm.taobao.com/bda/flow/flowmap/flow_map.htm?spm=a21ag.7622621.LeftMenu.d198.AuWNow#/?compare=source-self&device=1&keyword=flow-source'
driver.get(url)

def currentMonthFlowSource():    
    ##悬着无线
    driver.find_element_by_css_selector('div#flow-source-enter div.ui-switch.ui-switch-routable.btn-group-switch.device-group > ul > li:nth-child(2) > a').click()
    #点击日期框
    driver.find_element_by_css_selector(' div.ui-dropdown.can-select-again > a').click()
    #选择日期按钮
    driver.find_element_by_css_selector('article#main li:nth-child(4)').click()
    ##获取日期table
    tbody = driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-container > table.ui-calendar-date > tbody')
    current =  tbody.find_elements_by_css_selector('td.current-month')
    
    #遍历循环
    
    now = datetime.now()
    now = now.strftime('%Y-%m-%d')
    now = datetime.strptime(now,'%Y-%m-%d')
    
    for item in range(len(current)):
        data_value = current[item].get_attribute("data-value")
        date_value =datetime.strptime(data_value,'%Y-%m-%d')
        if date_value < now :
            current[item].get_attribute("data-value")
            #点击日期框
            driver.find_element_by_css_selector(' div.ui-dropdown.can-select-again > a').click()
            #选择日期按钮
            driver.find_element_by_css_selector('article#main li:nth-child(4)').click()
            
            driver.implicitly_wait(30)        
            ###########数据预处理
            #循环2次
            n=2
            for i in range(n):
                ##悬着无线
                try:
                    current[item].click()
                    break
                except:
                    time.sleep(5)
                    print('第-----' +str(i)+'click失败')
            try:
                platform = u'无线'
                driver.find_element_by_css_selector('div#flow-source-enter div.ui-switch.ui-switch-routable.btn-group-switch.device-group > ul > li:nth-child(2) > a').click()
        
                ##删除存在的文件
                info  = base.delete_xlsfile(path=path)
        
                #下载
                driver.find_element_by_css_selector('div#flow-source-enter div.source-tab > div.navbar > div > div.ui-download.navbar-download > a > span').click()
                #确定
                driver.find_element_by_css_selector('div#flow-source-enter div.ui-download.open.navbar-download > div > p > a.btn.btn-primary.btn-sm').click()
                time.sleep(3)
                platform = u'无线'  
                info_read,sheet=base.read_table(path=path,sheetname=0,skiprows=4)
                sheet[u'店铺']=business_name
                sheet[u'平台'] = platform
                #sheet[u'date'] = current[item].get_attribute("data-value")
                
                sever_table_name =business_name+platform+source                                 
                info_sql = base.to_mysql(local_table=sheet,server_table= sever_table_name)
                info = u'数据预处理成功'
                print('第-----' +str(i)+'-----' +info)
            except:
                info = u'数据预处理失败'
                print('第-----' +str(i)+'-----'+ info)
                