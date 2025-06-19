from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId, errors
from app.models.user import UserIn, Conversation, Message


async def insert_user(collection: AsyncIOMotorCollection, user: UserIn) -> str:
    result = await collection.insert_one(user.dict(by_alias=True, exclude_unset=True))
    return str(result.inserted_id)


async def get_user_by_id(collection: AsyncIOMotorCollection, user_id: str) -> dict | None:
    try:
        oid = ObjectId(user_id)
    except errors.InvalidId:
        return None
    return await collection.find_one({"_id": oid})


async def get_user_by_tg_id(collection: AsyncIOMotorCollection, tg_id: int) -> dict | None:
    return await collection.find_one({"tg_id": tg_id})


async def update_user(collection: AsyncIOMotorCollection, user_id: str, user: UserIn) -> bool:
    try:
        oid = ObjectId(user_id)
    except errors.InvalidId:
        return False
    result = await collection.replace_one({"_id": oid}, user.dict(by_alias=True, exclude_unset=True))
    return result.modified_count > 0


async def delete_user_by_id(collection: AsyncIOMotorCollection, user_id: str) -> bool:
    try:
        oid = ObjectId(user_id)
    except errors.InvalidId:
        return False
    result = await collection.delete_one({"_id": oid})
    return result.deleted_count > 0


async def delete_user_by_tg_id(collection: AsyncIOMotorCollection, tg_id: int) -> bool:
    result = await collection.delete_one({"tg_id": tg_id})
    return result.deleted_count > 0


async def add_conversation(collection: AsyncIOMotorCollection, user_id: str, conversation: Conversation) -> bool:
    try:
        oid = ObjectId(user_id)
    except errors.InvalidId:
        return False
    result = await collection.update_one(
        {"_id": oid},
        {"$push": {"conversations": conversation.dict(by_alias=True, exclude_unset=True)}}
    )
    return result.modified_count > 0


async def add_message_to_conversation(collection: AsyncIOMotorCollection, user_id: str, conv_index: int, message: Message) -> bool:
    try:
        oid = ObjectId(user_id)
    except errors.InvalidId:
        return False
    key = f"conversations.{conv_index}.messages"
    result = await collection.update_one(
        {"_id": oid},
        {"$push": {key: message.dict(by_alias=True, exclude_unset=True)}}
    )
    return result.modified_count > 0
