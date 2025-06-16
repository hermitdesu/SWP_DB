from motor.motor_asyncio import AsyncIOMotorCollection
from models.engagement import engagementIn

async def insert_engagement(collection: AsyncIOMotorCollection, engagement: engagementIn):
    result = await collection.insert_one(engagement.dict())
    return str(result.inserted_id)

async def get_engagement(collection: AsyncIOMotorCollection, id: str):
    return await collection.find_one({"id": id})

async def update_engagement(collection: AsyncIOMotorCollection, id: str, engagement: engagementIn):
    result = await collection.replace_one({"id": id}, engagement.dict())
    return result.modified_count

async def delete_engagement(collection: AsyncIOMotorCollection, id: str):
    result = await collection.delete_one({"id": id})
    return result.deleted_count
