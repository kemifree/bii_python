
<!-- toc orderedList:0 depthFrom:1 depthTo:6 -->

* [python --- pandas学习](#python-pandas学习)
  * [循环遍历读取文件夹](#循环遍历读取文件夹)
  * [读取excel数据](#读取excel数据)
  * [读取数据库mysql](#读取数据库mysql)
  * [mongb数据操作](#mongb数据操作)
    * [向mongodb写入数据](#向mongodb写入数据)
    * [从mongodb读取数据](#从mongodb读取数据)

<!-- tocstop -->


# python --- pandas学习
## 循环遍历读取文件夹
```python
import os
def delete_xlsfile(path):
    for root,dirs,files in os.walk(path):##文件夹的路径
        if files:   ##判断是否有文件
            for file_name in files:  ##循环文件的名称
                if '.xls' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                    xls_path = os.path.join(root,file_name)
                    print(xls_path)

                    taobao_directory = 'C:\\taobao_downloads' ##把文件copy到哪里？
                    if os.path.exists(taobao_directory):

                        shutil.copy(xls_path,taobao_directory)

                    else :
                        os.mkdir(taobao_directory)

                    os.remove(xls_path)
        temp_delete_info=u'xls文件清空完毕'
        return(temp_delete_info)
"""
path_downloads = 'C:\\Users\\Acer\\Downloads'
info  = delete_xlsfile(path=path_downloads)
"""
```



## 读取excel数据
``` python
-- 读取excel 数据
import pandas as pd
def read_xlsx(path,sheet_name):
    xlsx_file = pd.ExcelFile(path) ##路径
    xlsx_table = xlsx_file.parse(sheet_name) ##选取表格
    return(xlsx_table)
## 写入 将DataFrame数据写入到excel文件中
pd.to_excel('C:\\Users\\Acer\\Desktop\\phone_query.xlsx',encoding='utf-8')
 ```
## 读取数据库mysql
``` python
-- 方法一： pymysql
import pymysql
conn = pymysql.connect(host='172.16.57.72',
                             port=3306,
                             user='step',
                             password='123456',
                             db='tb_orders',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)                   
cursor = conn.cursor()
sql =  'select * from temp'
cursor.execute(sql)
data = cursor.fetchall()
df = pd.DataFrame(data)
-- 读取数据方式2 sqlalchemy
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tb_orders?charset=utf8")
sql = 'select * from temp'
df = pd.read_sql(sql,con=engine,chunksize=10000)
## 写入到数据库
df.to_sql('df_sql_name',con=engine,if_exists='replace',index=False,chunksize=10000)
```
## mongb数据操作
### 向mongodb写入数据
* 直接插入数据，不考虑数据是否重复；
``` python
def insert_mongb(posts):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.python
    table_phone = db.phone
    result = table_phone.insert_one(posts)
    return result
```
* 存在更更新，不存则插入数据
```python
def insert_mongb(post):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.taobao
    taobao_product = db.taobao_product
    result = taobao_product.update({'商品ID':post['商品ID']},{"$setOnInsert":post}, upsert=True)
    return result
```



### 从mongodb读取数据
```
def read_mongb():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.taobao
    taobao_product = db.taobao_product
    data = pd.DataFrame(pd.DataFrame(list(taobao_product.find())))
    return data
 ```
