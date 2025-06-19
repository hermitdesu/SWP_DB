import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = client.swp_db

user_collection = db.users
log_collection = db.logs
