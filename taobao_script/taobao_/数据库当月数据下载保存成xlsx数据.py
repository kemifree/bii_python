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


def search_table(db,table):
    month_date = datetime.date(datetime.now()).strftime('%Y-%m')
    print('现在的月份是' + str(month_date))

    server_con = "mysql+pymysql://step:123456@172.16.57.72/"+db+"?charset=utf8"
    engine = create_engine(server_con)
    sql = '''select * from  '''+ table + ''' where 日期 REGEXP  '%s' ''' %month_date 
    df = pd.read_sql(sql,con=engine)
    return df


if __name__ == "__main__":
    month_date = datetime.date(datetime.now()).strftime('%Y-%m')
    print('现在的月份是' + str(month_date))
    path = 'C:\\Users\\Acer\\Desktop\\运营明细表\\'
    db ={'boqii_c':'波奇C店',
     'boqii_jiafeimao':'加菲猫店',
     'boqii_shuizu':'水族',
     'boqii_tmall':'天猫旗舰店',
     'boqii_xincheng':'欣橙',
     'boqii_yiqin':'怡亲'}
    table = '运营明细表'
    for key in db:
        db_server = key
        db_name = db[key]
        df =search_table(db=db_server,table=table)
        file = db_name+'---'+table+'.xlsx'
        file_path = path+file
        df.to_excel(file_path,index=False)
        print('正在下载---'+db_name+'---'+table)