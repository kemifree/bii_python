# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:01:06 2017

@author: Acer
"""

##将近30天数据按照本月日期的数据插入到 自然月数据中
import time
import pandas as pd
from sqlalchemy import create_engine
import datetime

def read_mysql(db_name,db_table,duplicates_columns,server_table_name):
    con = "mysql+pymysql://step:123456@172.16.57.72/"+db_name+"?charset=utf8"
    engine = create_engine(con)
    sql = 'select *  from  '+ db_table
    table = pd.read_sql(sql,con=engine)
    df = table.drop_duplicates(duplicates_columns)
    df['月份'] =df['日期范围'].str.findall(r'\d{4}-\d{2}').str.get(0)
    df.to_sql(server_table_name,con=engine,if_exists='replace',index=False,chunksize=10000) 
    print('数据处理完成')


if __name__ == "__main__":
    start_time = time.time() # 开始时间
    db_name = 'tmall'
    duplicates_columns = ['所属终端','商品id','商品在线状态','日期类型','日期范围','店铺']
    server_table_name = '波奇网旗舰店商品效果自然月_近30天'
    ##
    db_table = '波奇网旗舰店商品效果最近30天'
    read_mysql(db_name,db_table,duplicates_columns,server_table_name)
    ##
    db_table = '波奇网旗舰店商品效果自然月'
    read_mysql(db_name,db_table,duplicates_columns,server_table_name)
    
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))

d = '2017-07-14'
datetime.strptime(d,'%Y-%m-%d')
datetime.datetime.strptime(d,'%Y-%m-%d')
df.index = df['日期']

df['dd'].to_period('M')

df['dd'] =pd.to_datetime(df['日期'])

pd.to_datetime(df['日期'], errors='ignore').month()
help(pd.to_datetime)