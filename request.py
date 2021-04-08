import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'H':3.45, 'D':2.75, 'A':2.25})

print(r.json())