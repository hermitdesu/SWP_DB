import requests

url = "https://swpdb-production.up.railway.app/logs/"

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

log_data = {
    "user_id": "user_id",
    "activity_id": "name",
    "type": "string",
    "value": "string",
    "start_time": "2025-06-20T10:11:15.012Z",
    "completion_time": "2025-06-20T10:11:15.012Z",
    "build_version": "string"
}

response = requests.post(url, json=log_data)

print(response.status_code)
print(response.text)
