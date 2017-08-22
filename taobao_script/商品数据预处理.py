# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:42:18 2017
##计算环比增加
@author: Acer
"""

import time
import pandas as pd
from sqlalchemy import create_engine
import numpy as np



def get_product():
    con = 'mysql+pymysql://step:123456@172.16.57.72/boqii_tmall?charset=utf8'
    engine = create_engine(con)
    #engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
    sql = 'select * from 天猫旗舰店商品信息表 '
    product = pd.read_sql(sql,con=engine)
    product = product.drop_duplicates(['商品ID'])
    product['商品id'] = product['商品ID'].astype(np.int64)
    #去除重复值
    return product    


def get_table_product(product_table,duplicates_columns,db_name,db_table):
    ##加载数据集    
    con = 'mysql+pymysql://step:123456@172.16.57.72/'+ db_name+'?charset=utf8'
    engine = create_engine(con)
    #engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
    sql = 'select * from '+  db_table
    table = pd.read_sql(sql,con=engine)
    table['日期'] = table['日期范围'].str.findall(r'\d{4}-\d{2}-\d{2}').str.get(1)
    ##增加商品属性
    table['商品id'] = table['商品id'].astype(np.int64)
    product_table['商品id'] = product_table['商品ID'].astype(np.int64)
    df = pd.merge(table,product_table,on ='商品id',how = 'left',suffixes=('_',''))
    df_columns = np.append(table.columns,['品牌','商品属性','货号'])
    df_indexes = np.unique(df_columns,return_index=True)[1]
    df_columns = [df_columns[index] for index in sorted(df_indexes)]
    df = df[df_columns]
    df.to_sql(db_table,con=engine,if_exists='replace',index=False,chunksize=10000) 
    print('增加商品属性完毕')

#duplicates_columns = ['店铺','商品在线状态','所属终端','商品id','日期']
def get_table_concat(duplicates_columns,db_name,db_table_1,db_table_2,server_table_name):
    ##加载数据集    
    con = 'mysql+pymysql://step:123456@172.16.57.72/'+ db_name+'?charset=utf8'
    engine = create_engine(con)
    #engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
    sql_1 = 'select * from '+  db_table_1
    table_1 = pd.read_sql(sql_1,con=engine)
    
    sql_2 = 'select * from '+  db_table_2
    table_2 = pd.read_sql(sql_2,con=engine)
    
    table = pd.concat([table_1,table_2])
    
    table = table.drop_duplicates(duplicates_columns)
    table['日期'] = table['日期范围'].str.findall(r'\d{4}-\d{2}-\d{2}').str.get(1)
    table.to_sql(server_table_name,con=engine,if_exists='replace',index=False,chunksize=10000) 
    print('表与表concat完毕')


#duplicates_columns = ['店铺','商品在线状态','所属终端','商品id','日期']

def get_table_pct(duplicates_columns,db_name,server_table_name):
    ##加载数据集    
    con = 'mysql+pymysql://step:123456@172.16.57.72/'+ db_name+'?charset=utf8'
    engine = create_engine(con)
    #engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tmall?charset=utf8")
    sql = 'select * from '+ server_table_name
    table = pd.read_sql(sql,con=engine)
    ## object --准换成float 做数学运算
    float_columns = ['访客数','支付金额','浏览量','支付买家数']    
    table[float_columns] = table[float_columns].astype(np.float64)  

    ##数据处理
    table =table.drop_duplicates(duplicates_columns)
    table['日期'] = table['日期范围'].str.findall(r'\d{4}-\d{2}-\d{2}').str.get(1)
    table['访客数_环比'] = table.sort_values('日期',ascending=True).groupby(['店铺','商品在线状态','所属终端','商品id']).访客数.pct_change()
    table['支付金额_环比'] = table.sort_values('日期',ascending=True).groupby(['店铺','商品在线状态','所属终端','商品id']).支付金额.pct_change()
    table['浏览量_环比'] = table.sort_values('日期',ascending=True).groupby(['店铺','商品在线状态','所属终端','商品id']).浏览量.pct_change()
    table['支付转化率_pd'] = table['支付买家数']/table['访客数']
    table['支付转化率_环比'] = table.sort_values('日期',ascending=True).groupby(['店铺','商品在线状态','所属终端','商品id']).支付转化率_pd.pct_change()
    table['详情页跳出率_pd'] = table['详情页跳出率'].str.findall(r'(\d+.\d+)').str.get(0) 
    #inf值替换
    table = table.replace([np.inf, -np.inf], np.nan)
    table.to_sql('server_table_name',con=engine,if_exists='replace',index=False,chunksize=10000)     
    print('增加环比变化')



if __name__ == "__main__":
    start_time = time.time() # 开始时间
    #商品表
    product_table = get_product()
    #
    db_name = 'tmall'
    duplicates_columns = ['店铺','商品在线状态','所属终端','商品id','日期']    
    ##增加商品属性信息
    db_table_30 = '波奇网旗舰店商品效果最近30天'
    get_table_product(product_table,duplicates_columns,db_name,db_table=db_table_30)
    db_table_month = '波奇网旗舰店商品效果自然月'
    get_table_product(product_table,duplicates_columns,db_name,db_table=db_table_month)

    db_table_week = '波奇网旗舰店商品效果自然周'
    get_table_product(product_table,duplicates_columns,db_name,db_table=db_table_week)
    db_table_7 = '波奇网旗舰店商品效果最近7天'
    get_table_product(product_table,duplicates_columns,db_name,db_table=db_table_7)
 
    ##表union
    db_table_1 = db_table_30
    db_table_2 = db_table_month
    server_table_name = '波奇网旗舰店商品效果自然月_近30天'
    get_table_concat(duplicates_columns,db_name,db_table_1,db_table_2,server_table_name)
    ##环比计算    

    #月环比
    server_table_name = db_table_month
    get_table_pct(duplicates_columns,db_name,server_table_name)
    #周环比
    server_table_name = db_table_week
    get_table_pct(duplicates_columns,db_name,server_table_name)