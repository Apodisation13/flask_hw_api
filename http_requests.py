import requests

HOST = 'http://127.0.0.1:5000'


r = requests.get(f'{HOST}/users/')
print(r.status_code)
