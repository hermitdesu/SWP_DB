<<<<<<< HEAD
import uvicorn
from fastapi import FastAPI
from routes.user_routes import router as user_router

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
=======
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

<<<<<<<< HEAD:app/db.py
client = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = client.swp_db

user_collection = db.users
log_collection = db.logs
========
cluster = AsyncIOMotorClient(os.getenv("MONGO_KEY"))
db = cluster.swp_db
>>>>>>>> 69b87370e0029a7a82f2246e530c9846565a90b6:app/main.py
>>>>>>> 69b87370e0029a7a82f2246e530c9846565a90b6
