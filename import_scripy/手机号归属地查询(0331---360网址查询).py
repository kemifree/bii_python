# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:22:49 2017
# 手机号码归属地调用示例代码 － 聚合数据
# 在线接口文档：360归属地查询
#http://cx.shouji.360.cn/phonearea.php?number=15340523553
#工具：requests
@author: Acer
"""
import requests
import pandas as pd
import json
import time
headers = {
    'Host':"cx.shouji.360.cn",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
    'Content-Type':"application/x-www-form-urlencoded",
    'Cookie':"__guid=167223102.590494287085193500.1484289762158.752; __gid=167223102.282731595.1484289762158.1484289830590.5; td_cookie=18446744072853883416; UM_distinctid=15b2253821921-019f73a19ba5a5-6a11157a-100200-15b2253821a259; __huid=11BOTV1QUhBuqvg3wkmWqnfm7R/Scz6z87yyEtnd1g7eo=",
    'Connection':"keep-alive",
    'Referer':'http://cx.shouji.360.cn/'
}
# 设置代理服务器
proxies= {
            'http:':'http://121.232.146.184',
            'https:':'https://144.255.48.197'
        }
        
def get_json(phone_number):
    data ={"number":phone_number}
    try:
        response = requests.post('http://cx.shouji.360.cn/phonearea.php', headers=headers, params=data,proxies = proxies)
    except Exception as e:
        print(e)
        s = requests.session()
        s.keep_alive = False
        response = requests.post('http://cx.shouji.360.cn/phonearea.php', headers=headers, params=data,proxies = proxies)
    return response.content
    
##方法一：对返回的json数据处理---
def get_number_info_one_way(phone_number):
    
    number = phone_number
    
    json_text = get_json(phone_number)
    
    json_dict = json.loads(json_text.decode())
    
    city =json_dict['data']['city']
    
    province = json_dict['data']['province']
    
    sp = json_dict['data']['sp']
    
    phone_info = pd.DataFrame({'number':[number],'city':[city],'province':[province],'sp':[sp]})
    
    return phone_info
##方法二；对返回的json数据处理---
def get_number_info_two_way(phone_number):

    json_text = get_json(phone_number)
    
    json_dict = json.loads(json_text.decode())
    
    columns = ['city','province','sp']
    
    phone_info = pd.DataFrame(json_dict['data'],columns=columns,index=[0])
    
    phone_info['number'] = phone_number

    return phone_info


def get_all_query(table,col_name):
    columns = columns = ['city','province','sp','number']
    
    phone_data = phone_data = pd.DataFrame([],columns=columns)
    
    for rows in  range(len(table)):
        print ('第'+str(rows)+'行---待查询号码---'+str(table.ix[rows,col_name]))
        phone_number = table.ix[rows,col_name]
        try:
            phone_info = get_number_info_two_way(phone_number)
        except:
            print('再次调用一次')
            phone_info = get_number_info_two_way(phone_number)
        phone_data = pd.concat([phone_data,phone_info])
    return phone_data


def read_xlsx(path,sheet_name):
    xlsx_file = pd.ExcelFile(path) ##路径
    xlsx_table = xlsx_file.parse(sheet_name) ##选取表格
    return(xlsx_table)
    
if __name__ == "__main__":
    start_time = time.time() # 开始时间
    path ='C:\\Users\\Acer\\Desktop\\phone.xlsx'
    sheet= 'Sheet1'
    col_name = 'phone'
    ##读取表格数据
    table = read_xlsx(path,sheet_name=sheet)
    #查询信息
    phone_data =get_all_query(table,col_name)
    #写入文件
    phone_data.to_excel('C:\\Users\\Acer\\Desktop\\phone_query.xlsx',encoding='utf-8')  
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))