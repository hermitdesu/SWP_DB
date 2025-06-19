import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = client.swp_db

users_collection = db.users
logs_collection = db.logs
