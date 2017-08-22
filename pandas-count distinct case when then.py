# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:55:15 2017

@author: Acer
"""
import pandas as pd
from datetime import datetime
df = pd.DataFrame([[101,1,'2017-07-01'],[101,2,'2017-07-12'],[101,3,'2017-07-20'],[101,4,'2017-07-21'],
                   [102,1,'2017-07-01'],[102,2,'2017-07-31'],[102,3,'2017-08-31'],
                    [103,1,'2017-07-30']],
                    columns = ['cust_id','apply_sequence','biz_grant_time'])
df                 
#日期处理
df['biz_month'] = df['biz_grant_time'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d').strftime('%Y-%m'))

df['apply'] =df['apply_sequence']
df['apply'][df['apply_sequence'] == 1] = '1次'
df['apply'][df['apply_sequence'] == 2] = '2次'
df['apply'][df['apply_sequence'] >= 3] = '3次及以上'

df
df.groupby(['biz_month','apply'])['cust_id'].nunique().unstack()

#索引重建
table  = df.groupby(['biz_month','apply'])['cust_id'].nunique().reset_index()



col = ['apply_sequence','cust_id']

pd.DataFrame(df,columns=col)


df.columns = col


obj = pd.Series([7,-5,7,4,2,0,4])
obj
obj.order()