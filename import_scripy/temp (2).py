# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import pandas as pd
import pymysql
import datetime


df = pd.DataFrame([['a',1],['a',2],['a',3],['b',3]], columns=['id', 'value'])

df

if __name__ == "__main__":
    start_time = time.time() # 开始时间
    path ='C:\\Users\\Acer\\Desktop\\'
    path ='C:\\Users\\Acer\\Desktop\\phone.xlsx'
    sheet= 'Sheet1'
    col_name = 'phone'
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))

def read_xlsx(path,sheet_name):
    xlsx_file = pd.ExcelFile(path) ##路径
    xlsx_table = xlsx_file.parse(sheet_name) ##选取表格
    
    xlsx_table.to_excel(path,sheet_name,index=False)
    return(xlsx_table)
    
def insert_mongb(posts):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.python
    table_phone = db.phone
    result = table_phone.insert_one(posts)
    return result

conn = pymysql.connect(host='172.16.57.72',
                             port=3306,
                             user='step',
                             password='123456',
                             db='tb_orders',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
##读取数据方式一                    
cursor = conn.cursor()
sql =  'select * from temp_0209_01 '
cursor.execute(sql)
data = cursor.fetchall()
table = pd.DataFrame(data)
##读取数据方式2
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tb_orders?charset=utf8")
sql = 'select taobaoshopname,uid from  tbcrmorder_201601 '
table = pd.read_sql(sql,con=engine)
#导入到mysql中
sheet.to_sql('tbcrmorder_orderstatus_2016',con=engine,if_exists='replace',index=False,chunksize=10000)



##pd.DataFrame操作
#一、删除重复项目；默认保留首次出现的值；
unique_df = table.drop_duplicates(['店铺','日期类型','日期','所属终端','商品id'])


