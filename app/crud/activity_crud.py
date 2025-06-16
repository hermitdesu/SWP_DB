from motor.motor_asyncio import AsyncIOMotorCollection
from models.activity import ActivityIn


async def insert_activity(collection : AsyncIOMotorCollection, activity : ActivityIn):
    result = await collection.insert_one(activity.dict())
    return str(result.inserted_id)

async def get_actitvity(collection : AsyncIOMotorCollection, activity_id : str):
    return await collection.find({"_id" : activity_id})

async def update_activity(collection: AsyncIOMotorCollection, activity_id: str, updated_activity: ActivityIn) -> int:
    result = await collection.replace_one({"id": activity_id}, updated_activity.dict())
    return result.modified_count

async def delete_activity(collection: AsyncIOMotorCollection, activity_id: str) -> int:
    result = await collection.delete_one({"id": activity_id})
    return result.deleted_count