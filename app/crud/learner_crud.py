from motor.motor_asyncio import AsyncIOMotorCollection
from models.learner import LearnerIn

async def insert_learner(collection: AsyncIOMotorCollection, learner: LearnerIn):
    result = await collection.insert_one(learner.dict())
    return str(result.inserted_id)

async def get_learner(collection: AsyncIOMotorCollection, id: str):
    return await collection.find_one({"id": id})

async def update_learner(collection: AsyncIOMotorCollection, id: str, learner: LearnerIn):
    result = await collection.replace_one({"id": id}, learner.dict())
    return result.modified_count

async def delete_learner(collection: AsyncIOMotorCollection, id: str):
    result = await collection.delete_one({"id": id})
    return result.deleted_count
