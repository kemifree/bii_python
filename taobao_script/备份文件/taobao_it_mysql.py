# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:10:03 2016

@author: Acer
"""
import pandas as pd

##读取数据
def read_csv(path):
    table = pd.read_csv(path,sep=",",index_col=False, encoding='utf-8',dtype='unicode',low_memory=False)
    return table
#将数据写入到数据库
import MySQLdb
from datetime import datetime
import sqlalchemy
from sqlalchemy.types import VARCHAR
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def write_sql_product(data,db_table):
    try:
        
        table=data
        
        dtype={dtype:VARCHAR(length=255) for dtype in table.columns}        
        
        engine=sqlalchemy.create_engine('mysql://step:123456@172.16.57.72:3306/tb_orders?charset=utf8',encoding='utf8')       
        table.to_sql(name=db_table,con=engine,flavor='mysql',if_exists='replace',index=False,chunksize=10000,dtype=dtype)   
        info =u'数据写入成功'
        print info
    except:
        info = u'数据写入失败'
        print info
    return info


def write_sql_orders(data,db_table):
    try:
        table=data
        dtype={dtype:VARCHAR(length=255) for dtype in table.columns} 
        dtype[u'address'] = VARCHAR(length=2550)
        dtype[u'taobaoUsername'] = VARCHAR(length=2550)
        dtype[u'taobaoTradeId'] = VARCHAR(length=2550)
        engine=sqlalchemy.create_engine('mysql://step:123456@172.16.57.72:3306/tb_orders?charset=utf8',encoding='utf8')       
        table.to_sql(name=db_table,con=engine,flavor='mysql',if_exists='replace',index=False,chunksize=10000,dtype=dtype)   
        info =u'数据写入成功'
        print info
    except:
        info = u'数据写入失败'
        print info
    return info

##读取订单数据写入数据库
path_orders = 'C:\\Users\\Acer\\Desktop\\tb_orders\\btCrmData20161227-1_75392\\log\\tbCrmData\\tbCrmOrder.csv'
path_orders = unicode(path_orders,encoding='utf-8')
orders_table = read_csv(path_orders)
orders_sql_info = write_sql_orders(data=orders_table,db_table=u'tbcrmorder_20161227')

##读取产品数据，写入数据库
path_prod = 'C:\\Users\\Acer\\Desktop\\tb_orders\\btCrmData20161227-1_75392\\log\\tbCrmData\\tbCrmOrdProd.csv'

path_prod = unicode(path_prod,encoding='utf-8')

prod_table = read_csv(path_prod)

product_info = write_sql_product(data=prod_table,db_table =u'tbcrmordprod_20161227')
        


