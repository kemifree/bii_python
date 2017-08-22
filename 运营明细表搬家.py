# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:53:29 2017

@author: Acer
"""

import time
import pandas as pd
import pymysql
from  datetime import datetime
from sqlalchemy import create_engine


def get_table(local_db,shop_name):
    server_con = "mysql+pymysql://boqii_mei:boqii123456@172.16.57.72/"+local_db+"?charset=utf8"
    engine = create_engine(server_con)
    sql = '''select * from  '''+ shop_name 
    df = pd.read_sql(sql,con=engine)
    engine.dispose()
    return df
def insert_boqii_server(data,server_db,shop_name):
    server_con = "mysql+pymysql://boqii_crm_tbuser:Hj5d46efs9d3Abg@172.16.76.132/"+server_db+"?charset=utf8"
    engine = create_engine(server_con)
    table_name = shop_name
    data.to_sql(table_name,con=engine,if_exists='replace',index=False,chunksize=10000)
    return '数据载入完成'
    engine.dispose()



if __name__ == "__main__":
    db = [{'boqii_tmall':'天猫旗舰店'},{'boqii_xincheng':'欣橙'},
      {'boqii_yiqin':'怡亲'},{'boqii_c':'波奇C店'},
      {'boqii_jiafeimao':'加菲猫店'},{'boqii_shuizu':'水族'}]
    table = '运营明细表'      
    for i in db:
        for key in i:
            db_server = key
            db_name = i[key]
            print(db_name)
            ##获取数据
            data =get_table(local_db=db_server,shop_name=table)
            ##存放到server
            shop_name = db_name+table
            server_db ='tb_crm'
            insert_boqii_server(data=data,server_db=server_db,shop_name=shop_name)


    
    
    