# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:33:34 2017

@author: Acer
"""
import pandas as pd
import time
from selenium import webdriver
from datetime import datetime
from sqlalchemy import create_engine
from numpy import nan
import pandas as pd
from sqlalchemy import create_engine
 
def login_boqii(username,password):
    
    ##下载路径位置和谷歌selenium驱动器位置
    options = webdriver.ChromeOptions()
    
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\Acer\\Downloads'}
    
    options.add_experimental_option('prefs', prefs)

    
    driver = webdriver.Chrome("C:\\Users\\Acer\\Desktop\\git\\selenium\\chromedriver_win32\\chromedriver.exe",chrome_options=options)
    
    driver.get('http://bqadmin.boqii.com/admin_login.php')
    
    
    driver.find_element_by_xpath('//*[@id="loginForm"]')
    
    #driver.switch_to.frame(frame)
    
    
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    

    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    return driver
'''

    #driver.find_element_by_xpath('//*[@id="sendsms"]').submit()
    ##
    #driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').submit()
    time.sleep(30)
    #print (driver.page_source)
    
    
    #driver.implicitly_wait(30)
    
    ##直接定位到主页
    #driver.get('https://sycm.taobao.com/portal/index.htm?spm=a21ag.8106233.logo.1.kxzbwq')
    cookie_list = driver.get_cookies()
    ##浏览器最大化
    driver.maximize_window()
    
    #temp_login_info='登陆成功'
    
    return(cookie_list,driver)
'''

def boqii_set(driver):
    url = 'http://bqadmin.boqii.com/index.php'
    driver.get(url)
    time.sleep(3)
    ##坑爹，先定位到框架
    frame = driver.find_element_by_xpath('//*[@id="leftFrame"]')
    driver.switch_to.frame(frame)
    driver.implicitly_wait(30)
    ##商品管理
    driver.find_element_by_css_selector('#backstage_left > dl > dd:nth-child(8) > a').click()
    #总商品列表
    driver.find_element_by_css_selector('#backstage_left > dl > dd:nth-child(8) > dl > dd:nth-child(3) > a').click()
    driver.implicitly_wait(30)
    ##切换到主文档-DOM树顶部
    driver.switch_to.default_content()
    #重新定位查询frame
    frame = driver.find_element_by_xpath('//*[@id="mainFrame"]')
    driver.switch_to.frame(frame)
    driver.implicitly_wait(30)
    time.sleep(1)
    #选择全部仓库
    driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[9]/td[2]/select').click()
    driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[9]/td[2]/select/option[1]').click()
    return driver
    
        
    
##
def query_stock(driver,taobaoid,productid):        
    stock = None
    taobaoid = str(taobaoid)
    productid = str(productid)
    #淘宝B店数字ID:
    #taobaoid ='552734775862'
    #taobaoid ='35035323499' #productid ='1125609'
    #商品编号 = 
    #productid ='1125609'
    ##查询框架
    while True:
        try:
            #淘宝B店数字ID
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[12]/td[1]').text
            #淘宝B店数字ID查询
            #输入产品id
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[12]/td[2]/input').send_keys(taobaoid)
            #淘宝B店数字ID查询
            driver.find_element_by_xpath('//*[@id="searchbutton"]').click()
            driver.implicitly_wait(30)
            #虚拟库存
            stock = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td[8]').text  
            print(str(taobaoid) + '商品库存---'+str(stock))
            #查询完后清除
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[12]/td[2]/input').clear()
            
            break
        except:
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[12]/td[2]/input').clear()
            print(str(taobaoid)+'淘宝ID查询无库存')
        #真坑爹，商品id查询无货，但是货号查询有货，需要查询两次

        try:
            #商品编号ID查询
            #输入产品id
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[5]/td[4]/input').send_keys(productid)
            #淘宝B店数字ID查询
            driver.find_element_by_xpath('//*[@id="searchbutton"]').click()
            driver.implicitly_wait(30)
            #虚拟库存
            stock = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td[8]').text  
            print(str(productid) + '商品库存---'+str(stock))            
            #真坑爹，商品id查询无货，但是货号查询有货，需要查询两次
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[5]/td[4]/input').clear() 
            break
        except:
            driver.find_element_by_xpath('//*[@id="form_search"]/table/tbody/tr[5]/td[4]/input').clear()
            print(str(productid) + '商品编号查询无库存')
            break
    return(stock)

def get_data():
    engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
    sql = '''select *  from  波奇网旗舰店商品效果最近30天  where 商品在线状态 = "已下架"  and 所属终端 ="所有终端"'''
    table = pd.read_sql(sql,con=engine)
    #导入到mysql中
    
    #table.drop_duplicates(['所属终端','商品id'])
    
    table.fillna(value=nan, inplace=True)
    
    table.dropna(subset=['货号'],how='all',inplace=True)
    #help(table.dropna)
    #删除Nan杭虎数据
    df = table[['日期范围', '店铺', '日期类型','所属终端','商品id','货号','商品标题', '商品在线状态', '商品链接', '浏览量', '访客数',
                '支付转化率','支付金额', '支付商品件数', '加购件数','收藏人数']]
    
    df = df.reset_index()
    return df




if __name__ == "__main__":
    start_time = time.time() # 开始时间
    username = 'vivian'
    password = 'vivian123'
    df = get_data()
    driver = login_boqii(username,password) ##登陆
    driver = boqii_set(driver)
    for i in range(len(df)):
        taobaoid = df.ix[i,'商品id']
        productid = df.ix[i,'货号']
        taobaoid,productid
        stock = query_stock(driver,taobaoid,productid)
        df.ix[i,'stock'] = stock
        #每运行100次，重置一次；
        if  i%100  == 0 and  i!=0:
            driver = boqii_set(driver)
        else:
            pass
    df.to_excel('C:\\Users\\Acer\\Desktop\\库存查询表.xlsx',index=False)