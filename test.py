import urllib.parse
import urllib.request
import json
import requests
import datetime
from docx import Document
from xlwt import *

# url = "http://127.0.0.1:5000/upload"
# files={'file':open('白鹿原_改.docx','rb')}
# response=requests.post(url,files=files).text
# print(response)

# document=Document('白鹿原_改.docx')
# for para in document.paragraphs:
#     print("!@3")
#     print(para.text)

import os

def read_ad_words():
    file=open('ad.txt',encoding="utf8").read()
    # print(file)
    dic={}
    for i in file.split('\n'):
        for i2 in i.split('|'):
            if len(i2)==0:
                continue
            dic.setdefault(i2,0)
            dic[i2]+=1
    dic=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    args=[]
    for i in dic:
        print(i)
        args.append([i[0]])
    import mySqlDB
    mySqlDB.insert_ad_words(args)

def read_sensitive_word():
    file=open('sensitive_words.txt',encoding="utf8").read()
    file_list=file.split("\n")
    args=[]
    for word in file_list:
        args.append([word])
    import mySqlDB
    mySqlDB.insert_sensitive_words(args)

read_sensitive_word()