# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:33:34 2017

@author: Acer
"""
import pandas as pd
import requests
import time
from selenium import webdriver
from datetime import datetime
from sqlalchemy import create_engine

def login_taobao(username,password):
    
    ##下载路径位置和谷歌selenium驱动器位置
    options = webdriver.ChromeOptions()
    
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\Acer\\Downloads'}
    
    options.add_experimental_option('prefs', prefs)

    
    driver = webdriver.Chrome("C:\\Users\\Acer\\Desktop\\git\\selenium\\chromedriver_win32\\chromedriver.exe",chrome_options=options)
    
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
    cookie_list = driver.get_cookies()
    ##浏览器最大化
    driver.maximize_window()
    
    #temp_login_info='登陆成功'
    
    return(cookie_list,driver)
def get_data(end_date):
    end_date = end_date
    series_date = pd.date_range(end = end_date,periods=30)
    df = pd.DataFrame(pd.Series(series_date),columns=['date'])
    ##最多请求七个
    '''
    indexCode ={
    'payAmt':'支付金额(元)',
    'uv':'访客数',
    'payRate':'支付转化率',
    'payPct':'客单价',
    'descScore':'描述相符评分',
    'rfdSucAmt':'成功退款金额(元)',
    'p4pExpendAmt':'直通车消耗',
    'payByrCnt':'支付买家数',
    'tkExpendAmt':'淘宝客佣金(元)',
    'zzExpendAmt':'钻石展位消耗(元)',
    'olderPayAmt':'老买家支付金额(元)',
    'payItmCnt':'支付件数',
    'payOldByrCnt':'支付老买家数',
    'payOrdCnt':'支付子订单数',
    'cartByrCnt':'加购人数',
    'cartCnt':'加购件数',
    'cltItmCnt':'商品收藏人数',
    'pv':'浏览量'
    }
    '''
    index_code ={
    'code_frist':'payAmt,uv,payRate,payPct,descScore',
    'code_four':'rfdSucAmt,p4pExpendAmt,payByrCnt',
    'code_second':'tkExpendAmt,zzExpendAmt,olderPayAmt',
    'code_five':'payItmCnt,payOldByrCnt',
    'code_third':'payOrdCnt,cartByrCnt,cartCnt,cltItmCnt,pv'
    }
    
    source ={
    "dateRange":end_date+str('|')+end_date,
    "dateType":"day",
    "device":"0",
    "includeRival":"false",
    "indexCode":'uv',
    "seller":"-1",
    "token":"42c42c264",
    "_":"1495422574255"
        }
    base_url = 'https://sycm.taobao.com/portal/coreIndex/getTrend.json?'
    try:
        for key in index_code:
            Code =index_code[key]
            indexCode ={'indexCode':Code}
            source.update(indexCode)
            #time.sleep(3)            
            ##判定地址解析是否成功
            for i in range(3):
                try:
                    response = session.get(base_url,headers = headers,params=source)
                    content = response.json()
                    data_values = content['content']['data']
                    time.sleep(3)
                    break
                except:
                    print('url解析失败')
                    
            ##数据处理
            #etl_df = pd.DataFrame(pd.Series(series_date),columns=['date'])
            #etl_df.index = pd.Series(series_date)
            for key_value in data_values:
                column = key_value
                value = data_values[key_value]['value']
                content_data = {column:value}
                temp_df = pd.DataFrame.from_dict(content_data)
                temp_df.index = series_date
                #time.sleep(3)
                print('---------------------'+column)
                df = pd.merge(df,temp_df,left_on = 'date',right_index=True)
    except:
        df = None
        print('失败')
    return(df)
    

if __name__ == "__main__": 
    username=u'波奇网旗舰店:zjq'
    password=u'a123456'
    cookies,driver = login_taobao(username,password)
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    headers={
    "accept":"*/*",
    "accept-encoding":"gzip, deflate, sdch, br",
    "accept-language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2",
    "referer":"https://sycm.taobao.com/mq/industry/overview/overview.htm?spm=a21ag.7782695.LeftMenu.d293.aaaYIy",
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    indexCodeName ={
    'date':'日期',
    'payAmt':'支付金额(元)',
    'uv':'访客数',
    'payRate':'支付转化率',
    'payPct':'客单价',
    'descScore':'描述相符评分',
    'rfdSucAmt':'成功退款金额(元)',
    'p4pExpendAmt':'直通车消耗',
    'payByrCnt':'支付买家数',
    'tkExpendAmt':'淘宝客佣金(元)',
    'zzExpendAmt':'钻石展位消耗(元)',
    'olderPayAmt':'老买家支付金额(元)',
    'payItmCnt':'支付件数',
    'payOldByrCnt':'支付老买家数',
    'payOrdCnt':'支付子订单数',
    'cartByrCnt':'加购人数',
    'cartCnt':'加购件数',
    'cltItmCnt':'商品收藏人数',
    'pv':'浏览量'
    }
    
    end_date = '2017-06-15'
    df = get_data(end_date)   
    df = df.drop_duplicates(['date'])
    df = df[[   'date','payAmt','uv',
                'payRate','payPct','descScore',
                'rfdSucAmt',
                'p4pExpendAmt',
                'payByrCnt','tkExpendAmt','zzExpendAmt',
                'olderPayAmt',
                'payItmCnt',
                'payOldByrCnt',
                'payOrdCnt','cartByrCnt',
                'cartCnt','cltItmCnt','pv'
        ]]
    #重新命名
    df =df.rename(columns =indexCodeName )
    ##设置小数位
    #如果是float类型，小数位取4位小数
    float_columns = df.dtypes.index [df.dtypes == float]
    decimal = pd.Series([4],index = float_columns)
    df.round(decimal)
    
    
    engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
    df.to_sql('运营报表',con=engine,if_exists='replace',index=False,chunksize=10000)
    
    
  



