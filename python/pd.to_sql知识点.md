# python向数据库写入数据

## 基础读取数据操作


## pymysql 读取数据  
```SQL
conn = pymysql.connect(host='172.16.57.72',
                             port=3306,
                             user='step',
                             password='123456',
                             db='tb_orders',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)                  
cursor = conn.cursor()
sql =  'select * from temp_0209_01 '
cursor.execute(sql)
data = cursor.fetchall()
table = pd.DataFrame(data)
```

## pd.reas_sql 读取数据
```SQL
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://step:123456@172.16.57.72/tb_orders?charset=utf8")
sql = 'select taobaoshopname,uid from  tbcrmorder_201601 '
table = pd.read_sql(sql,con=engine)

pd 保存到mysql
sheet.to_sql('tbcrmorder_orderstatus_2016',con=engine,if_exists='replace',index=False,chunksize=10000)
```

## 特殊情况处理
### df数据框 存在lnf 如何处理

* 提示：pd.to_sql 现在已经支持Nan数据存入到数据库，保存结果是NULL
* 报错提示：
```python
sqlalchemy.exc.InternalError: (pymysql.err.InternalError) (1054, "Unknown column 'inf' in 'field list'")
```
* 解决办法
将df数据框的 lnf 值替换成 Nan
```df.replace([np.inf, -np.inf], np.nan)```
