# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:02:38 2017

@author: Acer
"""

"""
Created on Wed Feb 15 14:18:35 2017
@author: Acer
"""
import pymysql
import pandas as pd
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
conn = pymysql.connect(host='172.16.57.72',
                             port=3306,
                             user='step',
                             password='123456',
                             db='tb_orders',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
sql = 'select * from  boqii_tbcrmordprod_20170201  limit 1000'
table = pd.read_sql(sql,con=conn)
productname = table['productName']
prod_list = productname.tolist()
import jieba
seg_list = jieba.cut(str(prod_list),cut_all=False)
text = " ".join(seg_list)
words = [word for word in jieba.cut(str(prod_list),cut_all=False) if len(word) >= 2]
df = pd.DataFrame(words)
df.columns = ['words']
words_counts = df.groupby('words').size()
words_counts.sort(inplace =True,ascending = False)
wordcloud = WordCloud(font_path="C:\\Users\\Acer\\Pictures\\simhei.ttf", background_color="black").generate(text)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()