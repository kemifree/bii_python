# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:34:03 2017

@author: Acer
"""
import os 
import smtplib
import email.mime.multipart
import email.mime.text
from email.header import Header
import pandas as pd
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication  
class send_email():
    def __init__(self):
        reporttime = datetime.today().strftime("%Y-%m-%d")
        self.receive=['',''] #收件人
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['from'] = '' #发件人

    def send(self):
        try:
            server = smtplib.SMTP()
            server.connect('smtp.exmail.qq.com', '465') #邮箱服务器和端口
            #server.connect('smtp.qq.com', '25') #邮箱服务器和端口
            server.login('ministep@boqii.net', 'Mini123456') #发件邮箱和登陆密码
            txt = email.mime.text.MIMEText(self.content)
            self.msg.attach(txt)
            self.msg['to'] = ','.join(self.receive)
            self.msg['from'] = ','.join('minisstep')
            self.msg['From']    = Header('数据支持部','utf-8')          
            self.msg['Subject'] = Header(self.subject, 'utf-8')
            server.sendmail('ministep@boqii.net', self.receive, self.msg.as_string())
            server.quit()
            print('发送成功')
        except:
            print('发送失败')
            raise

    def putfu(self,path):
        att1 = email.mime.text.MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename='+path
        self.msg.attach(att1)
        
    def putfile(self,path):
        part = MIMEApplication(open(path,'rb').read())  
        part.add_header('Content-Disposition', 'attachment', filename=path)  
        self.msg.attach(part)  