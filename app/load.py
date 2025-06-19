import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import UserIn
from models.log import LogIn
from cruds.user_crud import insert_user
from cruds.log_crud import insert_log
from routes.user_routes import app

# Загрузка переменных окружения
load_dotenv()

# Подключение к MongoDB
cluster = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = cluster.swp_db
user_collection = db.users
log_collection = db.logs


# =========================
# Нормализация данных
# =========================

def normalize_user(data: dict) -> dict:
    return {
        "tg_id": int(data.get("tg_id") or data.get("id") or 0),
        "name": data.get("name", "Unknown"),
        "surname": data.get("surname", "Unknown"),
        "gender": data.get("gender", "male"),
        "language": data.get("language", "en"),
        "recommendation_method": data.get("recommendation_method"),
        "launch_count": int(data.get("launch_count", 0)),
        "current_bundle_version": int(data.get("current_bundle_version", 0)),
        "bundle_version_at_install": int(
            data.get("bundle_version_at_install") or
            data.get("bundleVersionAtInstall") or
            0
        )
    }


def normalize_log(data: dict) -> dict:
    try:
        value = float(data.get("value", 0.0))
    except (ValueError, TypeError):
        value = 0.0

    try:
        start_time = datetime.fromisoformat(data.get("start_date"))
        completion_time = datetime.fromisoformat(data.get("completion_date"))
    except Exception as e:
        raise ValueError(f"Invalid datetime format: {e}")

    return {
        "user_id": str(data.get("learner_id", "")),  # теперь всегда str
        "activity_id": data.get("activity_id", ""),
        "type": data.get("type", ""),
        "value": value,
        "start_time": start_time,
        "completion_time": completion_time,
        "build_version": data.get("build_version")
    }




# =========================
# Загрузка данных
# =========================

async def load_users_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    for raw_user in raw_data:
        try:
            user_data = normalize_user(raw_user)
            user = UserIn(**user_data)
            user_id = await insert_user(user_collection, user)
            print(f"[USER] Inserted ID: {user_id}")
        except Exception as e:
            print(f"[USER ERROR] {raw_user} -> {e}")


async def load_logs_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    for raw_log in raw_data:
        try:
            log_data = normalize_log(raw_log)
            log = LogIn(**log_data)
            log_id = await insert_log(log_collection, log)
            print(f"[LOG] Inserted ID: {log_id}")
        except Exception as e:
            print(f"[LOG ERROR] {raw_log} -> {e}")


# =========================
# Главная функция
# ========================

async def main():
    await load_users_from_json("/home/desgun/Documents/programming/swp/app/data/namaz_learners_anon.json")
    await load_logs_from_json("/home/desgun/Documents/programming/swp/app/data/namaz_logs_anon.json")


if __name__ == "__main__":
    asyncio.run(main())
