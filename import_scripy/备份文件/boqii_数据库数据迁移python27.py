#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 12:00:49 2016
数据库数据迁移
@author: Acer
"""
#
import pandas as pd 
import MySQLdb
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

        
###############################################
def boqii_sql(db_name,db_table_name,server_business,server_table):
    try:
        boqii_con= MySQLdb.connect(host='172.16.57.72', charset='utf8',port=3306,user='step', passwd='123456', db=db_name)
        ##写SQL语句
        sql = 'select * from ' + '   ' + db_table_name
        ##读取数据
        table = pd.read_sql(sql,con=boqii_con)
        ##读取数据成功
        #print  u'数据读取成功'
    except :
        print u'数据读取失败'
    ##数据预处理
    try:
        table['日期'] = pd.to_datetime(table['日期'])
        boqii_table = table[table['日期']>pd.to_datetime('2000-10-16')]
        #print u'数据预处理成功'
    except:
        print u'数据处理失败'
    
    ##写入数据
    try:
        server_cn= MySQLdb.connect(host='172.16.57.72', charset='utf8',port=3306,user='step', passwd='123456', db='boqii_server')
        ##写数据
        table_name = server_business + server_table
        boqii_table.to_sql(name=table_name,con=server_cn,flavor='mysql',if_exists='replace',index=False,chunksize=10000 )
        #print u'数据写入成功'
    except MySQLdb.Error,e:
        print e.args[1]
        print u'数据读取失败'
        pass

###########################################################################
#波奇C店数据传输;
def boqii_c(business):
    ##这两句没有作用，其目的是辨识而已；
    business=business
    try:
        db=u'boqii_c'
        business =u'波奇c店_'  
        boqii_sql(db,'钻展明细表',business,'钻展')
        boqii_sql(db,'直通车明细表',business,'直通车')
        boqii_sql(db,'运营明细表',business,'运营')
        print business+u'数据传输---成功'
        return (business+u'数据传输---成功')
    except:
        business =u'波奇c店_'   
        print business+u'数据传输---失败'
        return( business+u'数据传输---失败')

###########################################################################
#'加菲猫'数据传输;
def boqii_jiafeimao(business):
    ##这两句没有作用，其目的是辨识而已；
    business=business
    try:
        db=u'boqii_jiafeimao'
        business =u'加菲猫_'  
        boqii_sql(db,'钻展明细表',business,'钻展')
        boqii_sql(db,'直通车明细表',business,'直通车')
        boqii_sql(db,'运营明细表',business,'运营')
        print business+u'数据传输---成功'
        return (business+u'数据传输---成功')
    except:
        db='boqii_jiafeimao'
        business =u'加菲猫_'  
        print business+u'数据传输---失败'
        return( business+u'数据传输---失败')
        
        
###########################################################################
#'水族小宠'数据传输;
def boqii_shuizu(business):
    ##这两句没有作用，其目的是辨识而已；
    business=business
    try:
        db='boqii_shuizu'
        business =u'水族小宠_' 
        boqii_sql(db,'钻展明细表',business,'钻展')
        boqii_sql(db,'直通车明细表',business,'直通车')
        boqii_sql(db,'运营明细表',business,'运营')

        print business+u'数据传输---成功'
        return (business+u'数据传输---成功')
    except:
        db='boqii_shuizu'
        business =u'水族小宠_' 
        print business+u'数据传输---失败'
        return( business+u'数据传输---失败')
        
#'波奇网旗舰店'数据传输;
def boqii_tmall(business):
    ##这两句没有作用，其目的是辨识而已；
    business=business
    try:
        db='boqii_tmall'
        business =u'波奇网旗舰店_'  
        boqii_sql(db,'钻展明细表',business,'钻展')
        boqii_sql(db,'直通车明细表',business,'直通车')
        boqii_sql(db,'运营明细表',business,'运营')
        
        print business+u'数据传输---成功'
        return (business+u'数据传输---成功')
    except:
         db='boqii_tmall'
         business =u'波奇网旗舰店_'  
         print business+u'数据传输---失败'
         return( business+u'数据传输---失败')    




###########################################################################
#'欣橙'数据传输;
def boqii_xincheng(business):
    ##这两句没有作用，其目的是辨识而已；
    business=business
    try:
        db='boqii_xincheng'
        business =u'欣橙_'  
        boqii_sql(db,'钻展明细表',business,'钻展')
        boqii_sql(db,'直通车明细表',business,'直通车')
        boqii_sql(db,'运营明细表',business,'运营')
        print business+u'数据传输---成功'
        return (business+u'数据传输---成功')
    except:
        db='boqii_xincheng'
        business =u'欣橙_'  
        print business+u'数据传输---失败'
        return( business+u'数据传输---失败')
        
###########################################################################
#'怡亲'数据传输;
def boqii_yiqin(business):
    ##这两句没有作用，其目的是辨识而已；
    business=business
    try:
        db='boqii_yiqin'
        business =u'怡亲_'  
        boqii_sql(db,'钻展明细表',business,'钻展')
        boqii_sql(db,'直通车明细表',business,'直通车')
        boqii_sql(db,'运营明细表',business,'运营')
        print business+u'数据传输---成功'
        return (business+u'数据传输---成功')
    except:
        db='boqii_yiqin'
        business =u'怡亲_'  
        print business+u'数据传输---失败'
        return( business+u'数据传输---失败')


    
tmall = boqii_tmall('波奇网旗舰店')    
xincheng = boqii_xincheng('欣橙')
shuizu = boqii_shuizu('水族')
jiafeimao = boqii_jiafeimao('加菲猫')
c_business = boqii_c('波奇c店')
yiqin =boqii_yiqin('怡亲')



