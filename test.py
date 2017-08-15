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

def read_sensitive_word_base64():
    import base64
    file=open('C:\\Users\sunkai\Desktop\敏感词\\bannedwords-master\\pub_banned_words.txt')
    file=file.read().split("\n")
    str = ''
    for word in file:
        str+=base64.b64decode(word).decode()
    print(str)
    file=open("敏感词.txt",'w')
    file.write(str)
    file.close()

def write_sensitive_words_with_type():
    file=open('敏感词库表统计.txt',encoding="utf8").read()
    type_dic={}
    for line in file.split("\n"):
        line=line.split(" ")
        if(len(line)==2):
            line[0]=line[0].replace("\ufeff","")
            type_dic.setdefault(line[0],[])
            type_dic[line[0]].append(line[1])
    args=[]
    for key,value in type_dic.items():
        for word in value:
            args.append((key,word))
    import mySqlDB
    mySqlDB.insert_sensitive_word(args)

write_sensitive_words_with_type()
# read_ad_words()
