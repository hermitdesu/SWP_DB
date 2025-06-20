from fastapi import APIRouter, Depends, HTTPException

from app.models.log import LogIn, LogDB, LogOut
from app.cruds.log_crud import insert_log, get_log, update_log, delete_log
from app.db import logs_collection

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.post("/", response_model=LogOut)
async def create_log(log: LogIn):
    inserted_id = await insert_log(logs_collection, log)
    log_doc = await get_log(logs_collection, inserted_id)
    if not log_doc:
        raise HTTPException(status_code=500, detail="Log creation failed")
    return LogOut(**log_doc)


@router.get("/{log_id}", response_model=LogDB)
async def read_log_by_id(log_id: str):
    log = await get_log(logs_collection, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return LogOut(**log)


@router.put("/{log_id}", response_model=bool)
async def update_log_by_id(log_id: str, log: LogIn):
    updated_count = await update_log(logs_collection, log_id, log)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Log not updated")
    return True


@router.delete("/{log_id}", response_model=bool)
async def delete_log_by_id(log_id: str):
    deleted_count = await delete_log(logs_collection, log_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Log not deleted")
    return True
