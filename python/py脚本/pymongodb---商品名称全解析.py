# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:40:50 2017
淘系产品品牌分析
@author: Acer
"""

import pandas as pd
import pymysql
import jieba
import jieba.posseg as pseg
import re
#----------------加载字典
engine = pymysql.connect(host='172.16.57.72',
                             port=3306,
                             user='step',
                             password='123456',
                             db='淘系数据模板表',
                             charset='utf8')
##获取淘系品牌表
sql ='select * from 淘系品牌表'                         
brand_dict = pd.read_sql(sql,con=engine)
brand_dict['brandname']= brand_dict['brandname'].apply(lambda x : x.lower())
brand_dict['brandname']= brand_dict['brandname'].apply(lambda x : re.sub(' ','',x))
brand_dict.head()
brand_dict.rename(columns ={'brandname':'word'},inplace =True)
     

## 获取关键词字典表
sql ='select * from 淘系关键词'                         
key_dict = pd.read_sql(sql,con=engine)
key_dict['keyword']= key_dict['keyword'].apply(lambda x : x.lower())
key_dict['keyword']= key_dict['keyword'].apply(lambda x : re.sub(' ','',x))

key_dict.head()
key_dict.rename(columns ={'keyword':'word','weight':'freq','class':'tag'},inplace =True)
     

def add_word(df):
    for i in range(len(df)):
        word = df.ix[i,'word']
        freq = df.ix[i,'freq']
        tag =df.ix[i,'tag']
        #去掉空格
        #字母全部转换成小写
        word = word.lower()
        word=re.sub(' ','',word)
        jieba.add_word(word,freq=freq,tag=tag)
        i=i+1
        print('-----------------'+str(i))
   

add_word(brand_dict)
add_word(key_dict)


def jieba_cut(text,cut_all=False):
    text=text.lower()
    text=re.sub(' ','',text)
    seg_list = jieba.lcut(text,cut_all = cut_all)
    return seg_list

##采集品牌

def look_brand(text):
    #去掉空格
    #字母全部转换成小写
    text=text.lower()
    text=re.sub(' ','',text)
    brand = {'brand':None}
    words = pseg.cut(text,HMM=True)
    for word, flag in words:
        #print('%s %s' % (word, flag))
        if flag == 'brandname':
            brand = word
            #获取父标签
            brand = brand_dict.father_brandname[brand_dict['word'] == word].values[0]
            return(brand)

##采集重量
def look_weight(text):
    weight = {'weight':None}
    pattern =re.compile("(\d+\.\d+[a-zA-Z0-9\-\.\_]+|\d+[a-zA-Z0-9\-\.\_]+)")
    text_number = re.findall(pattern,text)
    for m in text_number:
        if re.search('g|kg',m):
            weight = m
            return(weight)
##采集重量
def look_weight_g(text):
    weight = {'weight':None}
    pattern =re.compile("(\d+\.\d+[a-zA-Z0-9\-\.\_]+|\d+[a-zA-Z0-9\-\.\_]+)")
    text_number = re.findall(pattern,text)
    for m in text_number:
        #print(m)
        if re.search('\d+kg',m):
            weight['weight'] = re.search('\d+\.\d+|\d+',m).group()
            weight['weight']  = float(weight['weight']) *1000
            break
        elif re.search('\d+g',m):
            weight['weight'] = re.search('\d+\.\d+|\d+',m).group()
            weight['weight']  = float(weight['weight'])
            break
        else:
            weight['weight']=None
        #print(weight)
    return(weight.get('weight'))
## 采集宠物            
def look_pet(text):
    pet = {'pet':None}
    pattern =re.compile("(猫|狗|犬)")
    if re.search(pattern,text):
        pet['pet'] = re.search(pattern,text).group()
        if pet.get('pet') == '犬':
            pet['pet'] = '狗'
        return(pet.get('pet'))

def query_mysql(tablename,chunksize=100000):
    from sqlalchemy import create_engine
    engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tb_crm?charset=utf8"
    sql = 'select * from  ' + tablename
    chunk = pd.read_sql(sql,con=engine,chunksize=chunksize)
    for df in chunk:
        df['cut_false'] = df['productname'].apply(lambda x : jieba_cut(x,cut_all=False))
        df['cut_true'] = df['productname'].apply(lambda x : jieba_cut(x,cut_all=True))
        df['brand'] = df['productname'].apply(lambda x : look_brand(x))
        df['weightname'] = df['productname'].apply(lambda x : look_weight(x))
        df['weight'] = df['productname'].apply(lambda x : look_weight_g(x))
        df['pet'] = df['productname'].apply(lambda x : look_pet(x))
        df['ordertbcretime'] = pd.to_datetime(df['ordertbcretime'])
        df['paytime'] = pd.to_datetime(df['paytime'])
        df['orderimporttime'] = pd.to_datetime(df['orderimporttime'])
        df['_id'] = df['orderimporttime'].astype(str).str.cat(df['orderid'].astype(str), sep='').str.cat(df['taobaoshopname'].astype(str),sep='').str.cat(df['uniqueid'].astype(str), sep='')        
        ## 建立mongodb连接
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.tbcrm
        try:
            db.tbcrm_product.insert_many(df.to_dict('records'),ordered=False)
        except:
            pass
        ## 循环每一分块，再降数据插入到mongodb
        #方法一：
        """
        for i in range(len(df)):
                key = df[['orderimporttime','taobaoshopname','orderid','uniqueid']].to_dict('records')[i]
                data = df.to_dict('records')[i]
                results = db.tbcrm.update(key,{"$setOnInsert":data}, upsert=True)
        """
        #方法二：insert_mysql 湖绿插入错误的值
                
    client.close()
    return(chunk)
    
query_mysql('temp_20170417_tbcrm_copy')









