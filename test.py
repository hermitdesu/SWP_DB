import requests

url = "https://swpdb-production.up.railway.app/users/"

data = {
    "tg_id": 0,
    "name": "vasiliy",
    "surname": "kaizer",
    "gender": "male",
    "language": "en",
    "recommendation_method": "fixed",
    "launch_count": 10,
    "current_bundle_version": 1,
    "bundle_version_at_install": 1
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)
