import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_KEY")


if not MONGO_URI:
    raise ValueError("MONGODB_URI not set")


client = AsyncIOMotorClient(MONGO_URI)
db = client.swp_db

users_collection = db.users
logs_collection = db.logs
