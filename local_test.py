import requests

res = requests.get('http://127.0.0.1:8008')
print(res.content)