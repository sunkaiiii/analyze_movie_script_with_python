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
print(os.getcwd())