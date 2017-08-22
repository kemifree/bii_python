# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:28:56 2017

@author: Acer
"""

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



driver = webdriver.Chrome("C:\\Users\\Acer\\Desktop\\git\\selenium\\chromedriver_win32\\chromedriver.exe")

driver.get('https://sycm.taobao.com/custom/login.htm')


frame = driver.find_element_by_xpath('//*[@id="app"]/div/section[1]/div/div[1]/iframe')

driver.switch_to.frame(frame)

print ('temp1')

driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys(u'波奇网旗舰店:zjq')

print ('temp2')
driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(u'a123456')
print ('temp3')
##
driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').submit()
time.sleep(5)
#print (driver.page_source)

driver.implicitly_wait(30)

driver.get('https://sycm.taobao.com/portal/index.htm?spm=a21ag.8106233.logo.1.kxzbwq')

driver.implicitly_wait(30)

##############################
##我的报表
url='https://sycm.taobao.com/adm/user_report.htm?spm=a21ag.7622622.LeftMenu.d442.MdL2C7'
driver.get(url)

print ("浏览器最大化")
driver.maximize_window()


##
#driver.find_element_by_css_selector('a#title109125').text

##选取特定报表
driver.find_element_by_css_selector('div.report-title-list > a[title="日运营明细表"]').click()


##预览数据

driver.find_element_by_css_selector('div.report-overview.report-overview-active ul.report-option-list li.option-list-action a.btn.btn-primary.btn-primary-diy').click()

##下载全部数据

driver.find_element_by_css_selector('div.preview-action a.btn.btn-primary.pull-right').click()





driver.find_element_by_css_selector('div.report-overview.report-overview-active ul.report-option-list li.option-list-action a.btn.btn-primary.btn-primary-diy').text




driver.find_element_by_css_selector('div#\31 09125 a.btn.btn-primary.btn-primary-diy').text

driver.find_element_by_css_selector('div.report-overview-list span div.report-overview.report-overview-active' )
