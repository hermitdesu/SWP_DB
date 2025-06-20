import requests

url = "https://swpdb-production.up.railway.app/users/" + "685526bd7ae06434bc1ca2a3"

data = {
    "tg_id": 200,
    "name": "vasiliy",
    "surname": "kaizer",
    "gender": "male",
    "language": "en",
    "recommendation_method": "fixed",
    "launch_count": 10,
    "current_bundle_version": 1,
    "bundle_version_at_install": 1,
}

conv_data = {
        "messages": [
            {
                "sender": "user",   
                "text": "message",
                "time": "2025-06-02T08:47:49.655+00:00"
            }
        ]
    }

message_data = {
    "sender": "bot",
    "text": "new message",
    "time": "2025-06-02T08:47:49.655+00:00"
}

response = requests.get(url)

print(response.status_code)
print(response.text)
