# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 13:55:48 2017

@author: Acer
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:15:07 2017

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
                             db='temp_etl',
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

text = '法国皇家ROYAL CANIN 小型犬奶糕/怀孕/哺乳期母犬/离乳期幼犬奶糕1kg MIS30'



sql = "select * from  temp_20170618 ;"

sheet = pd.read_sql(sql,con = engine)
sheet['brand'] = sheet['productname'].apply(lambda x : look_brand(x))

sum_brand = sheet.groupby(['orderimporttime','taobaoshopname','brand'])[['number','cost']].sum()
sum_brand = sum_brand.reset_index()
sum_brand.head()

sum_brand = sum_brand.rename(columns = {'orderimporttime':'日期','taobaoshopname':'店铺','number':'件数','cost':'金额'})

sum_brand.to_excel('C:\\Users\\Acer\\Desktop\\2017年0618品牌销售件数及金额.xlsx',index=False)
sheet.to_excel('C:\\Users\\Acer\\Desktop\\2017年0618订单明细表.xlsx',index=False)


