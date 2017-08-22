# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 12:27:13 2017

@author: Acer
"""
from __future__ import unicode_literals
import sys,os
sys.path.append("../")
import shutil
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer




def chineseanalyzer(file_path,title,content,keywords):
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    ix = create_in('tmp', schema) # for create new index
    #ix = open_dir("tmp") # for read only
    writer = ix.writer()
    writer.add_document(
    title=title,
    path=file_path,
    content=content)
    
    writer.commit()
    searcher = ix.searcher()
    parser = QueryParser("content", schema=ix.schema)
    ##关键词
    search_content = ''    
    search_path =''
    search_title = ''
    message  = '关键词【不存在】文档中'
    message_logic = False #判断关键词是否存在
    for keyword in keywords:
        q = parser.parse(keyword)
        searcher_results = searcher.search(q)
        if searcher_results: 
            for hit in searcher_results:
                #print(hit.fields())
                search_content = hit['content']
                search_path  = hit['path']
                search_title = hit['title']
                message  = '关键词【存在】文档中'
                message_logic = True
                print(message)
                if message_logic == True :
                    break
            if message_logic == True :
                break
        else:
            continue
    print(message)
    return(search_content,search_title,message_logic,search_path) 
            #message  ='关键词不存在'
            #return(search_content,search_title,message,search_path) 
                    #return(search_content,search_title,message,search_path)
                    #return(search_content,search_title,message,search_path)
                



def text_analysis(from_path,to_path,keywords):
    for root,dirs,files in os.walk(from_path):##文件夹的路径
        if files:   ##判断是否有文件
            for file_name in files:  ##循环文件的名称
                if '.txt' in file_name:  ##判断以xlsx结尾的文件是否在文件名称中
                    file_path = os.path.join(root,file_name)
                    print(file_path)
                    print(file_name)
                    title = file_name
                    file_path = file_path
                    #读取文件
                    file_object = open(file_path)
                    try:
                        content = file_object.read()
                    finally:
                        file_object.close()
                    print(content)
                    
                    search_content,search_title,message_logic,search_path = chineseanalyzer(file_path,title,content,keywords)
                    if message_logic ==True:
                        if not os.path.exists(to_path):
                            os.mkdir(to_path)
                        shutil.copy(file_path,to_path)
                
keywords = ['华为','华为']
from_path ='C:\\Users\\Acer\\Desktop\\result_words'
to_path = 'C:\\Users\\Acer\\Desktop\\words04'

text_analysis(from_path,to_path,keywords)