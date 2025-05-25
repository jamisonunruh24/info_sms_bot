import requests

r = requests.post("http://localhost:5000/api/vape", json={
    "command": "vape give me a random number"
})

print(r.json()["message"])