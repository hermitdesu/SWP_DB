from fastapi import APIRouter, HTTPException
from app.models import UserIn, UserOut, UserDB
from app.db import users_collection
from app.cruds import create_user, read_user_by_id, update_user_by_id, delete_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserIn):
    user_db = UserDB(**user.model_dump())
    user_id = await create_user(users_collection, user_db)
    user_doc = await read_user_by_id(users_collection, user_id)

    if not user_doc:
        raise HTTPException(status_code=500, detail="User creation failed")

    return UserOut(**user_doc)


@router.get("/{user_id}", response_model=UserOut)
async def read_user_endpoint(user_id: int):
    user_doc = await read_user_by_id(users_collection, user_id)
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user_doc)


@router.put("/{user_id}", response_model=bool)
async def update_user_endpoint(user_id: int, user: UserDB):
    success = await update_user_by_id(users_collection, user_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="User not updated")
    return True


@router.delete("/{user_id}", response_model=bool)
async def delete_user_endpoint(user_id: int):
    success = await delete_user_by_id(users_collection, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return True