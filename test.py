import requests

url = "https://swpdb-production.up.railway.app/conversations/"

data = {
    "_id": 1000000000000,
    "name": "Ivan",
    "surname": "Ivanovich",
    "gender": "male",
    "language": "ru",
    "recommendation_method": "fixed",
    "launch_count": 5,
    "current_bundle_version": 239,
    "bundle_version_at_install": 239
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

conv = {
  "user_id": 4312
}

log_data = {
    "user_id": "user_id",
    "activity_id": "name",
    "type": "string",
    "value": "string",
    "start_time": "2025-06-20T10:11:15.012Z",
    "completion_time": "2025-06-20T10:11:15.012Z",
    "build_version": "string"
}

response = requests.post(url, json=conv)

print(response.status_code)
print(response.text)