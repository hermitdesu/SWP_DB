from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.user import UserIn, UserDB


async def create_user(collection: AsyncIOMotorCollection, user: UserDB) -> int | None:
    await collection.insert_one(user.model_dump(by_alias=True))
    return user.id


async def read_user_by_id(collection: AsyncIOMotorCollection, id: int) -> dict | None:
    return await collection.find_one({"_id": id})


async def update_user_by_id(collection: AsyncIOMotorCollection, id: int, user: UserDB) -> bool:
    result = await collection.replace_one({"_id": id}, user.model_dump(by_alias=True, exclude_unset=True))
    return result.modified_count > 0


async def delete_user_by_id(collection: AsyncIOMotorCollection, id: int) -> bool:
    result = await collection.delete_one({"_id": id})
    return result.deleted_count > 0