import requests

payload = {'username': '', 'password': ''}
response = requests.get("http://localhost:5000/chapelcredit", params=payload)
print response.json()
