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
                             db='tb_crm',
                             charset='utf8')

sql ='select * from brandname'                         
brand_dict = pd.read_sql(sql,con=engine)
brand_dict['brandname']= brand_dict['brandname'].apply(lambda x : x.lower())
brand_dict['brandname']= brand_dict['brandname'].apply(lambda x : re.sub(' ','',x))
   
def add_word(df):
    for i in range(len(df)):
        brand = df.ix[i,'brandname']
        freq = df.ix[i,'freq']
        tag =df.ix[i,'tag']
        #去掉空格
        #字母全部转换成小写
        brand = brand.lower()
        brand=re.sub(' ','',brand)
        jieba.add_word(brand,freq=freq,tag=tag)
        i=i+1
        print('-----------------'+str(i))
        
add_word(brand_dict)

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
            brand = brand_dict.father_brandname[brand_dict['brandname'] == word].values[0]
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
        elif re.search('\d+g',m):
            weight['weight'] = re.search('\d+\.\d+|\d+',m).group()
            weight['weight']  = float(weight['weight'])
        else:
            weight['weight']=None
        #print(weight)
    return(weight.get('weight'))

def look_pet(text):
    pet = {'pet':None}
    pattern =re.compile("(猫|狗|犬)")
    if re.search(pattern,text):
        pet['pet'] = re.search(pattern,text).group()
        if pet.get('pet') == '犬':
            pet['pet'] = '狗'
        return(pet.get('pet'))

##读取mysql数据
from datetime import datetime
from datetime import timedelta                           

def insert_update(n):
    now  = datetime.now().strftime('%Y-%m-%d')
    now_30 = datetime.strptime(now,'%Y-%m-%d')-timedelta(30)
    now_30 = now_30.strftime('%Y-%m-%d')
    engine = pymysql.connect(host='172.16.57.72',
                             port=3306,
                             user='step',
                             password='123456',
                             db='tb_crm',
                             charset='utf8')
    i =n
    cursor = engine.cursor()
    sql = "select * from tbcrm_copy where orderimporttime between '"+now_30  +"'  and  '"   + now+ "' ;"
    #sql = "select * from tbcrm_copy where orderimporttime between '2017-03-01' and '2017-04-01'"
    df = pd.read_sql(sql,con = engine,chunksize=5000)
    for sheet in df:
        sheet['brand'] = sheet['productname'].apply(lambda x : look_brand(x))
        sheet['weightname'] = sheet['productname'].apply(lambda x : look_weight(x))
        sheet['weight'] = sheet['productname'].apply(lambda x : look_weight_g(x))
        sheet['pet'] = sheet['productname'].apply(lambda x : look_pet(x))
        temp  = sheet.astype(object).where(pd.notnull(sheet), None)
        sheet = temp
        #sheet[['productname','brand']]
        sql  = """INSERT INTO tbcrm_copy(orderid, productid,standardid,ispresent,uniqueid,orderimporttime,
        brandname,weightname,weight,petname) VALUES(%s, %s, %s, %s,%s, %s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE brandname  =VALUES(brandname),weightname = VALUES(weightname),
        weight = VALUES(weight),petname = VALUES(petname)"""
        #session.exectue(query,sheet.orderid[i],sheet.productid[i],sheet.standard[i],sheet.ispresent[i],sheet.brand[i])
        param = sheet[['orderid','productid','standardid','ispresent','uniqueid','orderimporttime','brand','weightname','weight','pet']].values.tolist()
        cursor.executemany(sql, param)
        engine.commit()     
        i=i+1
        print('ok')
        print(str(i))
    cursor.close()
    return(i)
i = insert_update(0)    

'''
import threading
import time
import queue


if __name__ == "__main__":  
    import threading  
    t = threading.Thread(target=insert_update,args=(0,))  
    t.start()  
    t = threading.Thread(target=insert_update,args=(0,))  
    t.start()  
    t.join()  
'''