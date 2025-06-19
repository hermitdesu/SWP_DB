import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_KEY")
print("MONGO_KEY:", MONGO_URI)

client = AsyncIOMotorClient(MONGO_URI)
db = client.swp_db

users_collection = db.users
logs_collection = db.logs
