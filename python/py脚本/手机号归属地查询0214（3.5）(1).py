import json, urllib
import urllib 
import pandas as pd
#----------------------------------
# 手机号码归属地调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/11
#----------------------------------

def read_xlsx(path,sheet_name):
    xlsx_file = pd.ExcelFile(path) ##路径
    xlsx_table = xlsx_file.parse(sheet_name) ##选取表格
    return(xlsx_table)

#手机归属地查询
def phone_request(appkey, phone_number,m="GET"):
    url = "http://apis.juhe.cn/mobile/get"
    params = {
        "phone" : phone_number, #需要查询的手机号码或手机号码前7位
        "key" : appkey, #应用APPKEY(应用详细页查询)
        "dtype" : "", #返回数据的格式,xml或json，默认json
 
    }
    params =urllib.parse.urlencode(params)
    if m =="GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content.decode('utf-8'))
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print (res["result"])
            phone_temp = pd.DataFrame(res["result"],columns=['province','city','company','card'], index=[0])
            phone_temp['phone_number'] = phone_number
        else:
            phone_temp=pd.DataFrame([],columns=['province','city','company','card'], index=[0])
            print( "%s:%s" % (res["error_code"],res["reason"]))
    else:
        print ("request api error")
        
    return phone_temp

def phone_query(table,col_name):
    #初始化文件    
    phone_data = pd.DataFrame([],columns=['province','city','company','card','phone_number'])
    #循环遍历每一行数据：
    for rows in  range(len(table)):
        print (table.ix[rows,col_name])
        phone_number = table.ix[rows,col_name]
        phone_temp_temp = phone_request(appkey,phone_number,"GET")
        phone_data = pd.concat([phone_data,phone_temp_temp])
    ##文件写出
    print (phone_data)
    return(phone_data)
#----------------------------------
# 以上函数不用修改，只需修改下面配置即可
# 
#----------------------------------

#配置您申请的APPKey
appkey = "dfaa69afe296064dfc4284932ee02979"  
#配置读取文件
path  ='C:\\Users\\Administrator\\Desktop\\phone.xlsx'
sheet_name  = 'Sheet1'
table = read_xlsx(path,sheet_name)
col_name = 'phone'
##文件写出
phone_data_info = phone_query(table,col_name)
phone_data_info.to_excel('C:\\Users\\Administrator\\Desktop\\phone_query.xlsx',encoding='utf-8')    