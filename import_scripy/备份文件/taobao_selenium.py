# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 16:53:58 2017

模拟淘宝登陆，模拟自助取数--我的报表下载数据

@author: Acer
"""
import time
from selenium import webdriver


class Taobao(object):

    def login_taobao(self,username,password):
        
        driver = webdriver.Chrome("C:\\Users\\Acer\\Desktop\\git\\selenium\\chromedriver_win32\\chromedriver.exe")
        
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
        driver.maximize_window()
        
        temp_login_info='登陆成功'
        
        return(temp_login_info,driver)
    
    #username=u'波奇网旗舰店:zjq'
    
    #password=u'a123456'
       
    #login_info,driver = login_taobao(username,password)
    
    
    ##############################
    ##我的报表
    def quit_driver(self,driver):
        driver.quit()
        quit_info = '关闭浏览器'        
        return(quit_info)
    
    def downloads_taobao_xls(self,driver,url,title_name ):
        max_num = 5 
    
        for i in range(max_num):    
            try:
                url=url
                driver.get(url)    
                print ("浏览器最大化")
                driver.maximize_window()
                    
                ##选取特定报表
                driver.find_element_by_css_selector('div.report-title-list > a[title='+title_name+']').click()
                
                ##预览数据
                driver.implicitly_wait(30)
                
                time.sleep(3)
                driver.find_element_by_css_selector('div.report-overview.report-overview-active ul.report-option-list li.option-list-action a.btn.btn-primary.btn-primary-diy').click()
                
                ##下载全部数据
                
                driver.find_element_by_css_selector('div.preview-action a.btn.btn-primary.pull-right').click()
                
                info ='淘宝数据下载成功'
                
                break
            except:
                
                i=i-1
                
                info='淘宝数据下载失败'
            return(info)
        #driver.implicitly_wait(30)  
        #driver.quit()
    ###############################################
    ###############################################
    ###下载淘宝数据 
    
    #driver=driver
    #title_name = '日运营明细表'
    #title_name = '店铺分析日报'
    #url='https://sycm.taobao.com/adm/user_report.htm?spm=a21ag.7622622.LeftMenu.d442.MdL2C7'
       
    #info_taobal_xls = downloads_taobao_xls(driver=driver,url=url,title_name=title_name )

        
#taobao = Taobao()
#username=u'波奇网旗舰店:zjq'
#password=u'a123456'
#login_info,driver = taobao.login_taobao(username,password)
    







