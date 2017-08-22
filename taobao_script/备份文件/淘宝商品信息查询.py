# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:25:25 2017
##商品属性解析
@author: Acer
"""

import pandas as pd
from sqlalchemy import create_engine
import os 
import requests
from bs4 import  BeautifulSoup 
import re
import time
session = requests.session()

def insert_mongb(post):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.taobao
    taobao_product = db.taobao_product
    result = taobao_product.update({'商品ID':post['商品ID']},{"$setOnInsert":post}, upsert=True)
    return result

def get_product(url):
    response = session.get(url)    
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    items = soup.select('div.attributes-list ul#J_AttrUL li') 
    product = {}
    product['商品名称'] = soup.select('div.tb-detail-hd h1')[0].get_text(strip=True)
    product['商品ID'] = re.findall(r'id=(\d+)',url)[0]
    product['商品链接'] = url
    for item in items:
        attr = item.get_text(strip=True).replace('\xa0','').replace(' ','')
        attr = {attr.split(':')[0]:attr.split(':')[1]}
        product.update(attr)
    insert_mongb(product)
    



def get_url(db_name,db_table):
    con = "mysql+pymysql://step:123456@172.16.57.72/"+db_name+"?charset=utf8"
    engine = create_engine(con)
    sql = 'select *  from  '+ db_table
    table = pd.read_sql(sql,con=engine)
    #商品链接
    df = table.drop_duplicates(['商品链接','商品id'])
    url_list = df['商品链接']
    #解析
    for i in range(len(url_list)):
        print('url商品地址共有'+len(url_list),'正在解析第'+'---'+i)
        url = url_list[i]
        try:
            for j in range(5):
                try:
                    get_product(url)
                except:
                    pass
                
                break
                print('解析成功')
        except:
            print('解析失败')
            
            

def read_mongb():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.taobao
    taobao_product = db.taobao_product
    data = pd.DataFrame(pd.DataFrame(list(taobao_product.find())))
    return data
    
def insert_mysql(data,db_table_name):
    engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/boqii_tmall?charset=utf8")
    #导入到mysql中
    data.to_sql(db_table_name,con=engine,if_exists='replace',index=False,chunksize=10000)

    
if __name__ == "__main__":
    start_time = time.time() # 开始时间
    db_name = 'tmall'
    db_table = '波奇网旗舰店商品效果最近30天'
    ##商品信息解析
    get_url(db_name,db_table)
    ##商品信息读取
    data = read_mongb()
    ##存入到数据库
    db_table_name ='天猫旗舰店商品信息表'
    insert_mysql(data,db_table_name)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))