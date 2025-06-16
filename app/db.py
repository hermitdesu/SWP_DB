import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
from dotenv import load_dotenv
from crud.learner_crud import get_learner

load_dotenv()

cluster = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = cluster.namaz_db