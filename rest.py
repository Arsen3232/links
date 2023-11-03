import requests

res = requests.post("http://127.0.0.1:5000/api/menu/4", json={'name': 'HTML', 'videos': '35'})
res = requests.post("http://127.0.0.1:5000/api/menu/5", json={'name': 'CSS', 'videos': '40'})
print(res.json())
