from fastapi import APIRouter, HTTPException
from bson import ObjectId

from models.user import UserIn, UserDB, Conversation, Message
from cruds.user_crud import (
    insert_user, get_user_by_id, get_user_by_tg_id,
    update_user, delete_user_by_id, delete_user_by_tg_id,
    add_conversation, add_message_to_conversation
)
from db import user_collection

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserDB)
async def create_user(user: UserIn):
    inserted_id = await insert_user(user_collection, user)
    user_data = await get_user_by_id(user_collection, inserted_id)
    if not user_data:
        raise HTTPException(status_code=500, detail="User creation failed")
    return user_data


@router.get("/{user_id}", response_model=UserDB)
async def read_user_by_id(user_id: str):
    user = await get_user_by_id(user_collection, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/tg/{tg_id}", response_model=UserDB)
async def read_user_by_tg_id(tg_id: int):
    user = await get_user_by_tg_id(user_collection, tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=bool)
async def update_user_by_id(user_id: str, user: UserIn):
    success = await update_user(user_collection, user_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="User not updated")
    return True


@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    success = await delete_user_by_id(user_collection, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return True


@router.delete("/tg/{tg_id}", response_model=bool)
async def delete_user_by_telegram_id(tg_id: int):
    success = await delete_user_by_tg_id(user_collection, tg_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return True


@router.post("/{user_id}/conversations", response_model=bool)
async def add_new_conversation(user_id: str, conversation: Conversation):
    success = await add_conversation(user_collection, user_id, conversation)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or conversation not added")
    return True


@router.post("/{user_id}/conversations/{conv_index}/messages", response_model=bool)
async def add_message(user_id: str, conv_index: int, message: Message):
    success = await add_message_to_conversation(user_collection, user_id, conv_index, message)
    if not success:
        raise HTTPException(status_code=404, detail="User or conversation not found")
    return True
