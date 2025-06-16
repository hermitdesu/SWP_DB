import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

cluster = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = cluster.swp_db