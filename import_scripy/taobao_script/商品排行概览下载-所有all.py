# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:08:28 2017

@author: Acer
"""

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


#选择支付金额top15
def productDownload(driver):
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
            downloadPlatform()


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
            download(platform)



#要先选择top15

#选择月份

def month_download(url):
    driver.get(url)
    #选取商品排行概览
    driver.find_element_by_css_selector('div.component-overview-tops > div.ui-switch.nav.nav-blank > ul > li:nth-child(2)> a').click()
    #选择日期
    #driver.find_element_by_css_selector('#main > div > div.component-overview-tops > div.navbar > div > div.ui-datepicker.navbar-datepicker.day > div.ui-dropdown.can-select-again > a').click()
    #driver.find_element_by_css_selector('article#main div.ui-datepicker.navbar-datepicker.day > div.ui-dropdown.can-select-again > a').click()    
    driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[1]/div/div[1]/div[1]/a').click()    
    #选取日
    driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[1]/div/div[1]/div[1]/ul/li[4]/a').click()
    #driver.find_element_by_css_selector('#main > div > div.component-overview-tops > div.navbar > div > div.ui-datepicker.navbar-datepicker.day > div.ui-dropdown.can-select-again.open > ul > li:nth-child(4) > a').click()
    ##选取月份
    driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-pannel > span.ui-calendar-control.month').click()
    
    month = driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-container > table.ui-calendar-month > tbody ')
    
    month_element =  month.find_elements_by_css_selector('td.range-element')
    
    for i in range(len(month_element)):
          
        month_element[i].text
        #month_element[i].get_attribute('class')
        
        #if month_element[i].text in ['5月','6月']:
            
        if 'range-element'   in   month_element[i].get_attribute('class')    and  'disabled-element range-element' not in month_element[i].get_attribute('class'):
            print('元素可以被选取')
           
            n=2
            for n in range(n):
            ##选择无线
                try:
                    time.sleep(1)
                    month_element[i].text
                    month_element[i].click()
                    time.sleep(1)
                    #下载当月数据
                    productDownload(driver)
                    break
                except:
                    time.sleep(5)
                    print('第-----' +str(n)+'click月份失败')
        else:
            print('focus——month failed')
            
        #选取商品排行概览
        driver.find_element_by_css_selector('div.component-overview-tops > div.ui-switch.nav.nav-blank > ul > li:nth-child(2)> a').click()
        driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[1]/div/div[1]/div[1]/a').click()    
        #选取日
        driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/div[1]/div/div[1]/div[1]/ul/li[4]/a').click()
        ##选取月份
        driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-pannel > span.ui-calendar-control.month').click()
        
        month = driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-container > table.ui-calendar-month > tbody ')
    



if __name__ == "__main__":
    url = 'https://sycm.taobao.com/bda/items/itemanaly/item_summary.htm?spm=a21ag.7623880.TopMenu.d230.DyZiux'
    driver.get(url)
    month_download(url)
