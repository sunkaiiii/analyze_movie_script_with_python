import urllib.parse
import urllib.request
import json
import requests
URL = 'https://api-cn.faceplusplus.com/humanbodypp/beta/detect'  # fance++调用身体监测的地址
API_KEY = 'iJZuow0cOQez62sxfNdjzjwXkaX9y0rB'  # 申请的api的key
API_SECRET = 'gz_PVjfT8V7DrMxfAOpOreAwMN1L2dGY'  # 申请的api的secret

'''
暂时使用的base64将图片进行编码传输
还可以使用图片url、图片二进制进行传输，具体请参考官方文档
https://console.faceplusplus.com.cn/documents/7774430
'''
DATA = {
    'api_key': API_KEY,
    'api_secret': API_SECRET,
}
url = "http://127.0.0.1:5000/upload"
urldata = urllib.parse.urlencode(DATA)
urldata = urldata.encode('utf8')
files={'file':open('疯狂的石头.txt','rb')}
response=requests.post(url,files=files).text
print(response)
# with urllib.request.urlopen(url, urldata.) as f:
#     print(f.read())