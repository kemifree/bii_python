# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:49:55 2017

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
##入店关键词
url='https://sycm.taobao.com/bda/toolbox/keyword/keyword_assistant.htm?spm=a21ag.8106233.C_KeywordRank.d124825.cO14MH#/?device=1&page=searchKeyword'
driver.get(url)

print ("浏览器最大化")
driver.maximize_window()
##选取无线端
driver.find_element_by_css_selector('ul.ui-switch-menu >.ui-switch-item.ui-routable-item:nth-child(2) ').click()


##选取日期框
driver.find_element_by_css_selector('div.ui-dropdown.can-select-again a.btn.btn-dropdown').click()

##选取日期框--日

driver.find_element_by_css_selector('ul.ui-dropdown-menu.ui-dropdown-menu-left  > li:last-child').click()

##选择日期狂---日期狂--日

###选取日期框

data_table=driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/table[1]')


rows=data_table.find_elements_by_css_selector('tr.ui-calendar-date-column td.current-month')

disabled_rows = data_table.find_elements_by_css_selector('tr.ui-calendar-date-column td.current-month.disabled-element')


##循环遍历每各看到元素
for i in range(len(rows)-len(disabled_rows)):
    ##选取日期框
    driver.find_element_by_css_selector('div.ui-dropdown.can-select-again a.btn.btn-dropdown').click()
    ##选取日期框--日
    driver.find_element_by_css_selector('ul.ui-dropdown-menu.ui-dropdown-menu-left  > li:last-child').click()

    rows[i].text
    rows[i].get_attribute("data-value")
    rows[i].click()
    
    ##下载

    driver.find_element_by_css_selector('article#main div.search-keyword > div > div.navbar > div > div.ui-download.navbar-download > a > span').click()

    ##下载确定

    driver.find_element_by_css_selector('article#main div.ui-download.open.navbar-download > div > p > a.btn.btn-primary.btn-sm').click()




##下载

#driver.find_element_by_css_selector('article#main div.search-keyword > div > div.navbar > div > div.ui-download.navbar-download > a > span').click()

##下载确定

#driver.find_element_by_css_selector('article#main div.ui-download.open.navbar-download > div > p > a.btn.btn-primary.btn-sm').click()

##选取无线端
#driver.find_element_by_css_selector('ul.ui-switch-menu >.ui-switch-item.ui-routable-item:nth-child(2) ').click()

##选取日期框
#driver.find_element_by_css_selector('div.ui-dropdown.can-select-again a.btn.btn-dropdown').click()

##选取日期框--日

#driver.find_element_by_css_selector('ul.ui-dropdown-menu.ui-dropdown-menu-left  > li:last-child').click()


##选择日期狂---日期狂--年
#driver.find_element_by_xpath('//div[3]/div/div/span[3]').click()  ##

##选择日期狂---日期狂--具体年

#driver.find_element_by_xpath("//article[@id='main']/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]/table[3]/tbody/tr[3]/td[2]").click()  ##td[2]是2017年



#driver.find_element_by_xpath("//article[@id='main']/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]/table[3]/tbody/tr[3]/td[1]").click()  ##td[1]是2016年



##选择日期狂---日期狂--月


#driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[4]').click()


##选择日期狂---日期狂--具体的月份

#driver.find_element_by_css_selector('article#main div.ui-calendar.show.day > div.ui-calendar-container > table.ui-calendar-month > tbody > tr:nth-child(4) > td:nth-child(3)').click()


