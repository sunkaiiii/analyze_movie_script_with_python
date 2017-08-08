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

wb=Workbook()
table=wb.add_sheet('顺景表')
Workbook.height
style=XFStyle()
alignment=Alignment()
alignment.horz=Alignment.HORZ_CENTER
style.alignment=alignment
table.write_merge(2,3,0,0,'场景',style)
table.write_merge(2,3,1,1,'拍摄地点',style)
table.write_merge(2,3,2,2,'气氛',style)
table.write_merge(2,3,3,3,'页数/行',style)
table.write_merge(2,3,4,4,'主要内容',style)
table.write(2,5,'角色',style)
table.write(3,5,'演员',style)
index=6
name_list=['老大','老二','老三']
for role in name_list:
    table.write(2,index,role,style)
    index+=1
table.write(2,index,'特约及群众演员',style)
index+=1
table.write(2,index,'服化道',style)
index+=1
table.write_merge(2,3,index,index,'其他',style)
index+=1
table.write_merge(2,3,index,index,'计划时间',style)
index+=1
table.write_merge(2,3,index,index,'备注',style)
font=Font
table.write_merge(1,1,0,index,'《'+'test'+'》顺景表',style)
wb.save('test'+'.xls')