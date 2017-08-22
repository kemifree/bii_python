# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:39:22 2017
商品效果明细明细数据下载
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
source = '商品效果'

url = 'https://sycm.taobao.com/bda/items/effect/item_effect.htm?spm=a21ag.7634348.LeftMenu.d248.WLJON7#/?cateId=0&cateType=0&_k=jqk1c5'
driver.get(url)


def tbody_click(driver):
    #选取日期框
    driver.find_element_by_css_selector('#main > div > div.screen-header > div > div > div.dtpicker-main > span').click()
    #选日
    driver.find_element_by_css_selector('#main > div > div.screen-header > div > div > div.dtpicker-menu > ul > li:nth-child(4)').click()
    ##选取tbody框
    tbody = driver.find_element_by_css_selector('div.ui-calendar.show.day > div.ui-calendar-container > table.ui-calendar-date > tbody')
    current =  tbody.find_elements_by_css_selector('td.current-month')
    current[0].click()
    for item in range(len(current)):
        class_value = current[item].get_attribute("class")
        if  'current-month' in class_value and 'disabled-element' not in class_value :
            current[item].get_attribute("data-value")
            driver.implicitly_wait(30) 
            print(current[item].get_attribute("data-value"))
            #循环2次
            n=2
            for i in range(n):
                try:
                    #选择日期框
                    driver.find_element_by_css_selector('#main > div > div.screen-header > div > div > div.dtpicker-main > span').click()
                    driver.implicitly_wait(30)
                    current[item].click()
                    time.sleep(1)
                    break
                except:
                    time.sleep(1)
                    print('第-----' +str(i)+'click失败')
            #下载数据
            switch_download()

#tbody_click(driver)

#全部\pc\无线 按钮选择


def switch_download():
    ui_switch_menu =['全部','无线','PC']
    for switch in ui_switch_menu:
        switch
        if switch == '全部':
            driver.find_element_by_css_selector('div.ui-switch.btn-group-switch > ul > li:nth-child(1)').click()
            download()
        elif switch == 'PC':
            driver.find_element_by_css_selector('div.ui-switch.btn-group-switch > ul > li:nth-child(2)').click()
            download()
        elif switch == '无线':
            driver.find_element_by_css_selector('div.ui-switch.btn-group-switch > ul > li:nth-child(3)').click()
            download()
#下载

def download():
    try:
        ##删除存在的文件
        info  = base.delete_xlsfile(path=path) 
        #下载数据    
        driver.find_element_by_css_selector('#main > div > div.component-effect > div.navbar > div > div.ui-download.btn-download > a').click()
        
        #确定
        driver.find_element_by_css_selector('#main > div > div.component-effect > div.navbar > div > div.ui-download.open.btn-download > div > p > a.btn.btn-primary.btn-sm').click()
        time.sleep(5)
        #platform = u'支付金额排行TOP15'
        for i in range(5):
            try:
                info_read,sheet=base.read_table(path=path,sheetname=0,skiprows=3)
                break
            except:
                print('文件正在下载中ing')
            
        sheet[u'店铺']=business_name
        sheet[u'日期类型']='自然日'
        #sheet[platform] = platform #表中已经自带渠道
        
        sever_table_name =business_name+source                                 
        info = base.to_mysql(local_table=sheet,server_table= sever_table_name)
        #info = u'数据预处理成功'
        print('第----------' +info)
    except:
        info = u'数据预处理失败'
        print('第----------'+ info)  
   
   
#文件是否下载成功检测
if __name__ == "__main__":
    n = 3 
    for i in range(n):
        try:
            url = 'https://sycm.taobao.com/bda/items/effect/item_effect.htm?spm=a21ag.7634348.LeftMenu.d248.WLJON7#/?cateId=0&cateType=0&_k=jqk1c5'
            driver.get(url)
            tbody_click(driver)
            break
        except:
            print('tobdy_click 暂时失败，正在重新运行')