import urllib.parse
import urllib.request
import json
url = "http://127.0.0.1:5000/hello"
with urllib.request.urlopen(url) as f:
    print(f.read().decode('utf-8'))