# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:34:03 2017

@author: Acer
"""

import smtplib
import email.mime.multipart
import email.mime.text
from email.header import Header
import pandas as pd
from datetime import datetime
import os 
import requests
from email.mime.application import MIMEApplication 
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from bs4 import  BeautifulSoup 


class send_email():
    def __init__(self):
        reporttime = datetime.today().strftime("%Y-%m-%d")
        self.receive=['',''] #收件人
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['from'] = '' #发件人

    def send(self):
        try:
            server = smtplib.SMTP()
            server.connect('smtp.exmail.qq.com', '25') #邮箱服务器和端口
            server.login('ministep@boqii.net', 'Mini123456') #发件邮箱和登陆密码
            txt = email.mime.text.MIMEText(self.content,'html', 'utf-8')
            self.msg.attach(txt)
            self.msg['From'] = Header('数据支持部', 'utf-8')
            self.msg['To'] = ','.join(self.receive)
            self.msg['Subject'] = Header(self.subject, 'utf-8')
            server.sendmail('ministep@boqii.net', self.receive, self.msg.as_string())
            server.quit()
            print('发送成功')
        except:
            print('发送失败')
            raise

    def putfu(self,path):
        filename = os.path.basename(path)
        att1 = email.mime.text.MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename='+filename
        self.msg.attach(att1)
        
    def put_xlsx(self,path):
        file_name = os.path.basename(path)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(path, "rb").read())
        encoders.encode_base64(part)
        part["Content-Type"] = 'application/octet-stream'
        part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
        #part.add_header('Content-Disposition', 'attachment; filename="operate.xlsx"')
        #part.add_header('Content-Disposition', 'attachment; filename="%s"'%Header(filename,'utf-8'))
        self.msg.attach(part)
     
    def weather(self):
        response = requests.get('http://weather.sina.com.cn/pudong')    
        response.encoding = 'utf-8'    
        html = response.text
        soup = BeautifulSoup(html,'lxml')
        city = soup.select('h4.slider_ct_name')[0].get_text()
        date = soup.select('p.slider_ct_date')[0].get_text()
        degree = soup.select('div.slider_degree')[0].get_text()
        detail = soup.select('p.slider_detail')[0].get_text(strip=True).replace('\xa0','').replace(' ','')
        return city,date,degree,detail  