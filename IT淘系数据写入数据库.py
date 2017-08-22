# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:10:03 2016

@author: Acer
"""
import pandas as pd



##读取数据
def read_data(path):
    table = pd.read_table(path,sep=",",index_col=False, dtype='unicode')
    return table

#将数据写入到数据库
import MySQLdb
from datetime import datetime
import sqlalchemy
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import TEXT
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def write_sql_product(data,db_table):
    try:
        
        table=data
        
        dtype={dtype:VARCHAR(length=255) for dtype in table.columns}        
        
        engine=sqlalchemy.create_engine('mysql://root:mini123456@localhost:3306/tb_orders?charset=utf8',encoding='utf8')       
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
        engine=sqlalchemy.create_engine('mysql://root:mini123456@localhost:3306/louis?charset=utf8',encoding='utf8')       
        table.to_sql(name=db_table,con=engine,flavor='mysql',if_exists='replace',index=False,chunksize=10000,dtype=dtype)   
        info =u'数据写入成功'
        print info
    except:
        info = u'数据写入失败'
        print info
    return info



##读取产品数据，写入数据库
path = 'C:\\Users\\Acer\\Desktop\\tbCrmOrdProd\\tbCrmOrdProd.txt'

path = unicode(path,encoding='utf-8')

table = read_data(path)

product_info = write_sql_product(data=table,db_table =u'tbcrmordprod')
        


##读取订单数据写入数据库
path = 'C:\\Users\\Acer\\Desktop\\tbCrmOrdProd\\tbCrmOrder.txt'
path = unicode(path,encoding='utf-8')
orders_table = read_data(path)

orders_sql_info = write_sql_orders(data=orders_table,db_table=u'tbCrmOrder')

data=orders_table
db_table='tbCrmOrder01'