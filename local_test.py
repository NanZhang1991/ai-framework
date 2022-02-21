import requests

res = requests.get('http://127.0.0.1:8000')
print(res.content)

res2 = requests.get('http://127.0.0.1:8000',data={'data':'text'})
print(res2.content)
