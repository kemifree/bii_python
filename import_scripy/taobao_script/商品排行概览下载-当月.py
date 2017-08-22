# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 16:12:18 2017
商品排行概览
支付金额top15
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
source = '商品排行概览'
url = 'https://sycm.taobao.com/bda/items/itemanaly/item_summary.htm?spm=a21ag.7623880.TopMenu.d230.DyZiux'
driver.get(url)

#选择支付金额top15
def productDownload(driver):
    #选择日期
    driver.find_element_by_css_selector('#main > div > div.component-overview-tops > div.navbar > div > div.ui-datepicker.navbar-datepicker.last1 > div.ui-dropdown.can-select-again > a').click()
    #选取日
    driver.find_element_by_css_selector(' div > div.ui-datepicker.navbar-datepicker.last1 > div.ui-dropdown.can-select-again.open > ul > li:nth-child(4)').click()
    
    #选取table
    tbody = driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-container > table.ui-calendar-date > tbody')
    current =  tbody.find_elements_by_css_selector('td.current-month')
    current[0].click()
    for item in range(len(current)):
        class_value = current[item].get_attribute("class")
        if  'current-month' in class_value and 'disabled-element' not in class_value :
            current[item].get_attribute("data-value")
            driver.implicitly_wait(30)        
            #循环2次
            n=2
            for i in range(n):
                try:
                    #选择日期框
                    driver.find_element_by_css_selector('div.ui-datepicker.navbar-datepicker.day > span').click()
                    driver.implicitly_wait(30)
                    current[item].click()
                    break
                except:
                    time.sleep(1)
                    print('第-----' +str(i)+'click失败')
            #下载-确认数据
            #downloadPlatform() #调用自己编写的函数


def download(platform):
    try:
        ##删除存在的文件
        info  = base.delete_xlsfile(path=path) 
        #下载数据    
        driver.find_element_by_css_selector('#main > div > div.component-overview-tops > div.navbar > div > div.ui-download.navbar-download > a').click()
        #确定
        driver.find_element_by_css_selector('article#main div.ui-download.open.navbar-download > div > p > a.btn.btn-primary.btn-sm').click()
        time.sleep(3)
        #platform = u'支付金额排行TOP15'
        info_read,sheet=base.read_table(path=path,sheetname=0,skiprows=3)
        sheet[u'店铺']=business_name
        sheet[platform] = platform
        
        sever_table_name =business_name+platform+source                                 
        info_sql = base.to_mysql(local_table=sheet,server_table= sever_table_name)
        #info = u'数据预处理成功'
        #print('第----------' +info)
    except:
        info = u'数据预处理失败'
        print('第----------'+ info)   





def downloadPlatform():
    #platform = u'支付金额排行TOP15'
    platform_dict ={'1':'支付金额排行TOP15','2':'访客数排行TOP15'}
    for key in platform_dict:
        if int(key) == 1:
            platform = platform_dict[key]
            driver.find_element_by_css_selector('div.component-overview-tops > div.ui-switch.nav.nav-blank > ul > li:nth-child(1)> a').click()
            download(platform)
        elif int(key) == 2:
            platform = platform_dict[key]
            driver.find_element_by_css_selector('div.component-overview-tops > div.ui-switch.nav.nav-blank > ul > li:nth-child(2)> a').click()
            download(platform) ##调用download自己编写的函数



if __name__ == "__main__":
    productDownload(driver)

