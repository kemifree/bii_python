# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:04:45 2017

@author: Acer
"""
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome("C:\\Users\\Acer\\Desktop\\git\\selenium\\chromedriver_win32\\chromedriver.exe")

#回复帖子

url = 'http://bbs.vlan5.com/thread-26013-1-1.html'

driver.get(url)

driver.find_element_by_xpath('//*[@id="fastpostmessage"]').send_keys("工程师论坛V5，加油，赞一个")

driver.find_element_by_xpath('//*[@id="fastpostsubmit"]/strong').click()
text_info = ['工程师论坛V5，加油',
        '工程师论坛，历史',
        'python大全(约10套视频+书籍打包下载',
                  '我今天最想说:「上攻城狮论坛bbs.vlan5.com,小菜鸟终将会成为大神!」',
                  '我在 2017-01-21 00:04 完成签到,获得随机奖励 金币 5',
                  '今天心情不错,嘿嘿!!!',
                  '过来看看的,感谢攻城狮论坛']

random.sample(text_info,1)

for i in range(30):
    
    one_package = random.sample(text_info,1)
    driver.find_element_by_xpath('//*[@id="fastpostmessage"]').send_keys(one_package)
    
    driver.find_element_by_xpath('//*[@id="fastpostsubmit"]/strong').click()
    
    time.sleep(11)
    
    print(i)
    
    
    
##开心灌水
    
water_message = ['开心灌水，开心灌水',
                 '开心灌输，哇哈哈',
                 '攻城狮，开心灌水',
                 '开心灌水007',
                 '开心灌水,有道理',
                 '开心灌水,感谢攻城狮论坛',
                 '开心灌水,好好 学习了 确实不错',
                 '开心灌水, 确实不错',
                 '开心灌水,攻城狮论坛一直',
                 '开心灌水,沙发！沙发!',
                 '开心灌水,坛客服报名CCN',
                 '谢谢楼主，共同发',
                 '路过，支持一下啦',
                 '希望越办越好']

for i in range(10):    
    time.sleep(1)
    
    url = 'http://bbs.vlan5.com/forum.php?mod=post&action=newthread&fid=58'
    
    driver.get(url)
    
    time.sleep(3)
    driver.implicitly_wait(30)
    #driver.find_element_by_xpath('//*[@id="newspecial"]/img').click()
    
    ##下拉
    driver.find_element_by_xpath('//*[@id="typeid_ctrl"]').click()
    
    ##开心灌水
    driver.find_element_by_css_selector('div#typeid_ctrl_menu li:nth-child(4)').click()
    
    

    
    
    one_messge = random.sample(water_message,1)
    
    driver.find_element_by_xpath('//*[@id="subject"]').send_keys(one_messge)
    
    #driver.find_element_by_xpath('//*[@id="subject"]').clear()
    #driver.find_element_by_css_selector('div#postbox button.pn.pnc > span').send_keys(one_messge)
    
    frame   = driver.find_element_by_xpath('//*[@id="e_iframe"]')
    
    
    driver.switch_to.frame(frame)
    
    driver.find_element_by_xpath('/html/body').send_keys(one_messge)
    
    #driver.find_element_by_css_selector('div#postbox button.pn.pnc > span').text
    
    driver.switch_to.default_content()
    
    driver.find_element_by_xpath('//*[@id="postsubmit"]/span').click()
    
    time.sleep(11)
    
    print(i)


