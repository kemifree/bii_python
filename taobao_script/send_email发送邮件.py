# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:34:03 2017

@author: Acer
"""


import sys
python_path = 'C:\\Users\\Acer\\Desktop\\import_scripy\\taobao_script\\'
sys.path.append(python_path)

import auto_email
import pandas as pd
from datetime import datetime


mail = auto_email.send_email()

ss = pd.read_csv('C:\\Users\\Acer\\Desktop\\0710.csv',encoding = 'gbk')

today = datetime.today().strftime("%Y-%m-%d")

weather = mail.weather()
weather = str(weather)

if isinstance(ss,str):
    mail.content = "no data! (′⌒`)"
else:
    email = '''
    <h1>您好,</h1>
        <p>附件已添加至附件中，请查收！</p>
        
        <p>天气预报：%s</p>
        
        <p>附注：表格简要信息如下</p>
        {ss} '''%(weather)
    mail.content = email.format(ss=ss.head(1).to_html())

 
mail.receive=['1679830748@qq.com']

mail.subject ='日常报表'

mail.putfu('C:\\Users\\Acer\\Desktop\\0710.csv')

mail.send()


